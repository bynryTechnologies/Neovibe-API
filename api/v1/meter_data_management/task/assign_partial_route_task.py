__author__ = "aki"

# API Header
# Package: Basic
# Modules: All
# Sub Module: All
# Usage: This task is used to assign partial task according route.
# Tables used: ConsumerDetail, RouteTaskAssignment, JobCardTemplate
# Author: Akshay
# Created on: 04/03/2021

import datetime
from celery.task import task
from fcm_django.models import FCMDevice
from v1.commonapp.views.logger import logger
from v1.meter_data_management.models.consumer_detail import ConsumerDetail as ConsumerDetailTbl
from v1.meter_data_management.models.meter_reading import MeterReading as MeterReadingTbl
from v1.meter_data_management.models.job_card_template import JobCardTemplate as JobCardTemplateTbl
from v1.meter_data_management.models.read_cycle import get_read_cycle_by_id
from v1.meter_data_management.models.route_task_assignment import get_route_task_assignment_by_id, \
    ROUTE_TASK_ASSIGNMENT_STATUS_DICT
from v1.meter_data_management.models.route import get_route_by_id
from v1.meter_data_management.models.spot_bill import get_spot_bill_by_consumer_detail_id

# Todo send id_string to mobile and pending notification code
@task(name="assign-partial-route-task", queue='Dispatch_I')
def assign_partial_route_task(route_task_assignment_id):
    try:
        time = datetime.datetime.now().time().strftime("%H %M")
        t = time.split(" ")
        time_to_sent = t[0] + ':' + t[1]
        task_data_list = []

        route_task_assignment_obj = get_route_task_assignment_by_id(route_task_assignment_id)

        task_obj = [x for x in route_task_assignment_obj.consumer_meter_json if x['is_active'] == True and
                       x['is_completed'] == False and x['is_revisit'] == False]

        if len(task_obj) == 0:
            task_template_obj = JobCardTemplateTbl.objects.get(tenant=route_task_assignment_obj.tenant,
                                                               utility=route_task_assignment_obj.utility,
                                                               is_active=True)

            consumer_detail_obj = ConsumerDetailTbl.objects.filter(route_id=route_task_assignment_obj.route_id,
                                                                   schedule_log_id=route_task_assignment_obj.schedule_log_id,
                                                                   utility_product_id=route_task_assignment_obj.utility_product_id,
                                                                   state=0, is_active=True)
            for consumer in consumer_detail_obj:
                try:
                    meter_reading_obj = MeterReadingTbl.objects.get(route_id=route_task_assignment_obj.route_id,
                                                                    consumer_detail_id=consumer.id, is_active=True,
                                                                    is_duplicate=False)
                except MeterReadingTbl.DoesNotExist:
                    task_dict = {
                        "consumer_no": consumer.consumer_no,
                        "meter_no": consumer.meter_no,
                        "consumer_detail_id": consumer.id,
                        "schedule_log_id": consumer.schedule_log_id,
                        "read_cycle_id": consumer.read_cycle_id,
                        "route_id": consumer.route_id,
                        "premise_id": consumer.premise_id,
                        "activity_type_id": consumer.activity_type_id,
                        "utility_product_id": consumer.utility_product_id,
                        "route_task_assignment_id": route_task_assignment_obj.id,
                        "meter_reader_id": route_task_assignment_obj.meter_reader_id,
                        "is_active": True,
                        "is_completed": False,
                        "is_revisit": False,
                        "status": 'ALLOCATED',
                        "task_template_meter_json": task_template_obj.meter_read_json_obj,
                        "task_template_additional_parameter_json": task_template_obj.additional_parameter_json
                    }

                    if consumer.is_spot_bill:
                        spot_bill_obj = get_spot_bill_by_consumer_detail_id(consumer.id)
                        task_dict['is_spot_bill'] = True
                        task_dict['spot_bill_detail'] = spot_bill_obj.spot_bill_detail
                        task_dict['rate_detail'] = spot_bill_obj.rate_detail

                    task_data_list.append(task_dict)

            route_task_assignment_obj.consumer_meter_json = task_data_list
        else:
            for task in task_obj:
                task['status'] = 'ALLOCATED'
                task['meter_reader_id'] = route_task_assignment_obj.meter_reader_id

        route_task_assignment_obj.change_state(ROUTE_TASK_ASSIGNMENT_STATUS_DICT["STARTED"])
        route_task_assignment_obj.save()

        read_cycle_obj = get_read_cycle_by_id(route_task_assignment_obj.read_cycle_id)

        route_obj = get_route_by_id(route_task_assignment_obj.route_id)

        message = "For Read Cycle - " + read_cycle_obj.name + " | Route - " + route_obj.label + " | Consumers - " + \
                  str(len(task_obj)) + " Are Assigned To You. Please Press Refresh Button.(Time : " + \
                  time_to_sent + ")"

        try:
            device = FCMDevice.objects.get(user_id=route_task_assignment_obj.meter_reader_id)
            try:
                device.send_message(title='Notification-Assign', body=message)
            except Exception as ex:
                print(ex)
                logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')
        except Exception as ex:
            print(ex)
            logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')

    except Exception as ex:
        print(ex)
        logger().log(ex, 'MEDIUM', module='CONSUMER OPS', sub_module='METER DATA')

        route_task_assignment_obj = get_route_task_assignment_by_id(route_task_assignment_id)

        task_obj = [x for x in route_task_assignment_obj.consumer_meter_json if x['is_active'] == True and
                    x['is_completed'] == False and x['is_revisit'] == False]

        complete_task_obj = [x for x in route_task_assignment_obj.consumer_meter_json if x['is_active'] == True and
                    x['is_completed'] == True and x['is_revisit'] == False]

        if len(complete_task_obj) == 0:
            route_task_assignment_obj.change_state(ROUTE_TASK_ASSIGNMENT_STATUS_DICT["NOT-DISPATCHED"])
        else:
            route_task_assignment_obj.change_state(ROUTE_TASK_ASSIGNMENT_STATUS_DICT["PARTIAL"])

        for task in task_obj:
            task['status'] = 'ALLOCATED'
            task['meter_reader_id'] = None

        route_task_assignment_obj.meter_reader_id = None
        route_task_assignment_obj.save()
