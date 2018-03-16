import butlerian

_JOB_NAME_ENV = 'PI_LIT_JOB_NAME'
_APP_NAME_ENV = 'PI_LIT_APP_NAME'


class MissingParameterException(Exception):
    def __init__(self, message):
        super(MissingParameterException, self).__init__(message)


if __name__ == '__main__':
    import os

    job_name = os.getenv(_JOB_NAME_ENV)
    app_name = os.getenv(_APP_NAME_ENV)

    if not job_name or not app_name:
        raise MissingParameterException("Error: environment variables {} and {} must be set."
                                        .format(_JOB_NAME_ENV, _APP_NAME_ENV))

    jenkins = butlerian.JenkinsApi()
    job = jenkins.get_job(job_name)
    for build in job.builds:
        print build
