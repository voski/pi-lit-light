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
    job = jenkins.get_job(job_name, app_name)
    if job.builds:
        # Get most recent build.
        build = job.builds[0]
        print 'Build:\t', build.full_display_name
        print 'Status:\t',
        if build.building:
            print 'yellow'  # Change the color to yellow
            pass
        elif build.result == 'SUCCESS':
            print 'green'   # Green
            #os.system('omxplayer -o local test.mp3')
            pass
        elif build.result == 'FAILURE':
            print 'red'     # Red
            pass
    else:
        # error message
        pass
