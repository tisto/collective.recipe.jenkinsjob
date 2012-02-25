Supported options
=================

The recipe supports the following options:

hostname
    Hostname of the Jenkins instance.

jobname
    Name of the Jenkins job.

username
    Jenkins username

password
    Jenkins password


Example usage
=============

We'll start by creating a buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = test1
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
	>>> "updating jenkins-job" in buildout_output_lower
	True
