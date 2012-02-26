Introduction
============

Simple buildout recipe that generated three commands *push a jenkins job*, *pull a jenkins job* and *trigger build on jenkins job*.

Recipe enables developer to sync configuration on Jenkins with buildout configuration.

Workflow to be used with the recipe:

- create and configure a job through the web
- run pull jenkins job
- later, make more changes the job through the web
- run pull jenkins job and use your SCM to diff the config
- (optional) push configuration to any other server or use it as restore
- (optional) trigger build, because you are too lazy to wait n minutes for cronjob

Supported options
=================

The recipe supports the following options:

hostname (required)
    Hostname of the Jenkins instance.

jobname (required)
    Name of the Jenkins job.

username (required)
    Jenkins username

password (required)
    Jenkins password

port (default: 80)
    Jenkins port

config_name (default: jenkins_config.xml)
    Name for XML configuration file for the Jenkins job


Example usage
=============

We'll start by creating a buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = jenkins-job
    ...
    ... [jenkins-job]
    ... recipe = collective.recipe.jenkinsjob
    ... hostname = %(hostname)s
    ... jobname = %(jobname)s
    ... username = %(username)s
    ... password = %(password)s
    ... """ % {
    ...     'hostname' : 'jenkins.plone.org',
    ...     'jobname' : 'Plone42',
    ...     'username': 'chuck',
    ...     'password': 'norris'})

Running the buildout gives us::

	>>> buildout_output_lower = system(buildout).lower()
	>>> "installing jenkins-job" in buildout_output_lower
	True
	>>> "generated script" in buildout_output_lower
	True
	>>> "bin/jenkins-job-push" in buildout_output_lower
	True
	>>> "bin/jenkins-job-pull" in buildout_output_lower
	True
	>>> "bin/jenkins-job-trigger-build" in buildout_output_lower
	True
