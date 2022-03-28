"""Views module."""

from flask import render_template, flash, url_for, request
from dependency_injector.wiring import inject, Provide
from werkzeug.utils import redirect
from prometheus_client import Counter, Summary

from app.src.services import app_health, instance_shutdown_scheduling
from app.src.services.instance_actions import InstanceActions
from app.src.services.instance_data import InstanceData
from app.containers import Container

from botocore.exceptions import ClientError

from flask.views import MethodView

import logging

logger = logging.getLogger()


class InstanceAPI(MethodView):
    @inject
    def __init__(self, instance_actions: InstanceActions = Provide[Container.instance_actions]) -> None:
        self.instance_actions = instance_actions
        super().__init__()

    def get(self, instance_id, instance_action):
        try:
            action_to_run = self.instance_actions.action_selector(
                instance_action)
            action_to_run(instance_id)
            flash("Your request to {} instance {} is in progress".format(
                instance_action, instance_id), "info")
        except (ClientError, RuntimeError) as e:
            flash("Cannot perform action '{}' on instance: {}".format(
                instance_action, instance_id), "danger")
            logger.exception(e)

        return redirect(url_for('instances'))

    def post(self, instance_id, instance_action):
        try:
            action_to_run = self.instance_actions.action_selector(
                instance_action)
            action_to_run(instance_id)
            flash("Your request to {} instance {} is in progress".format(
                instance_action, instance_id), "info")
        except (ClientError, RuntimeError) as e:
            flash("Cannot perform action '{}' on instance: {}".format(
                instance_action, instance_id), "danger")
            logger.exception(e)

        return redirect(url_for('instances'))


REQUESTS_COUNTER = Counter(
    'number_of_requests', 'The total number of requests per-page', ['method', 'endpoint'])
REQUEST_TIME = Summary('time_processing_request',
                       'The time spent processing a request', ['endpoint'])

HOME_REQUEST_TIME = REQUEST_TIME.labels(endpoint='home')


@HOME_REQUEST_TIME.time()
def home():
    logger.info("Home view")
    REQUESTS_COUNTER.labels(method='GET', endpoint='home').inc(1)
    return render_template('home.html', title='Welcome to Kandula')


ABOUT_REQUEST_TIME = REQUEST_TIME.labels(endpoint='about')


@ABOUT_REQUEST_TIME.time()
def about():
    REQUESTS_COUNTER.labels(method='GET', endpoint='about').inc(1)
    return render_template('about.html', title='About')


HEALTH_REQUEST_TIME = REQUEST_TIME.labels(endpoint='health')


@HEALTH_REQUEST_TIME.time()
def health():
    health_metrics, is_app_healthy = app_health.get_app_health()
    REQUESTS_COUNTER.labels(method='GET', endpoint='health').inc(1)
    return render_template('health.html', title='Application Health',
                           healthchecks=health_metrics), 200 if is_app_healthy else 500


INSTANCES_REQUEST_TIME = REQUEST_TIME.labels(endpoint='metrics')


@INSTANCES_REQUEST_TIME.time()
def metrics():
    REQUESTS_COUNTER.labels(method='GET', endpoint='metrics').inc(1)
    return render_template('metrics.html', title='metrics')


INSTANCES_REQUEST_TIME = REQUEST_TIME.labels(endpoint='instances')


@INSTANCES_REQUEST_TIME.time()
def instances(instance_data: InstanceData = Provide[Container.instance_data]):
    instances_response = instance_data.get_instances()
    REQUESTS_COUNTER.labels(method='GET', endpoint='instances').inc(1)
    return render_template('instances.html', title='Instances', instances=instances_response['Instances'])


SCHEDULER_REQUEST_TIME = REQUEST_TIME.labels(endpoint='scheduler')


@SCHEDULER_REQUEST_TIME.time()
def scheduler():
    if request.method == 'POST':
        instance_shutdown_scheduling.handle_instance(request.form)

    scheduled_instances = instance_shutdown_scheduling.get_scheduled_instances()
    REQUESTS_COUNTER.labels(method='GET', endpoint='scheduler').inc(1)
    return render_template('scheduler.html', title='Scheduling', scheduled_instances=scheduled_instances["Instances"])
