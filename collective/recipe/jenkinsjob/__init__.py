# -*- coding: utf-8 -*-
"""Recipe Jenkinsjob"""
import os
import jenkins

import zc.recipe.egg
from zc.buildout import UserError


class Recipe(object):
    """Recipe to configure Jenkins CI jobs.
    """

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.egg = zc.recipe.egg.Scripts(
            buildout,
            self.options['recipe'],
            options)

        # Check required options
        required_options = ['hostname', 'jobname', 'username', 'password']
        for required_option in required_options:
            if required_option not in self.options:
                raise UserError(
                    'Please provide a "%s" in your jenkins section "%s"' % (
                    required_option,
                    self.options['recipe']))

        # Set default options
        self.options.setdefault('port', '80')
        self.options.setdefault(
            'template',
            os.path.join(os.path.dirname(__file__),
            'default_config.xml.in'))
        self.options.setdefault('config_name', 'jenkins_config.xml')
        self.options.setdefault('username', '')
        self.options.setdefault('password', '')

        # Figure out default output file
        plone_jenkins = os.path.join(
            self.buildout['buildout']['parts-directory'], __name__)
        if not os.path.exists(plone_jenkins):
            os.makedirs(plone_jenkins)

        # Setup input/output file
        self.options['input'] = self.options['template']
        self.options['output'] = os.path.join(
            plone_jenkins,
            self.options['config_name'])

        # What files are tracked by this recipe
        self.files = [plone_jenkins,
            os.path.join(
                self.buildout['buildout']['bin-directory'], self.name)]

    def install(self):
        """Installer"""
        self.render_jenkins_config()
        self.install_scripts()

        # Return files that were created by the recipe. The buildout
        # will remove all returned files upon reinstall.
        return self.files

    def update(self):
        """Updater"""
        self.install()

    def install_scripts(self):
        """Install a jenkins-job script in the bin directory.
        """
        zc.buildout.easy_install.scripts(
            [(
                self.name,
                'collective.recipe.jenkinsjob',
                'create_jenkins_job'
            )],
            self.egg.working_set()[1],
            self.buildout[self.buildout['buildout']['python']]['executable'],
            self.buildout['buildout']['bin-directory'],
            arguments=self.options.__repr__(),
        )

    def render_jenkins_config(self):
        """Render the Jenkins job configuration.
        """
        #g = GenshiRecipe(self.buildout, self.name, self.options)
        #g.install()
        pass


def create_jenkins_job(options):
    """Script that pushes a job to the Jenkins CI server.
    """
    # Variables
    jenkins_url = options['hostname']
    jenkins_username = options['username']
    jenkins_password = options['password']
    jenkins_jobname = options['jobname']
    jenkins_config = open("jenkins.xml").read()

    # Connect to Jenkins CI server
    jenkins_server = jenkins.Jenkins(
        jenkins_url,
        jenkins_username,
        jenkins_password)

    # Create Jenkins job
    if jenkins_server.job_exists(jenkins_jobname):
        print(
            "Reconfig Job %s" %
            jenkins_server.get_job_info(jenkins_jobname)['url'])
        try:
            jenkins_server.reconfig_job(jenkins_jobname, jenkins_config)
        except jenkins.JenkinsException, e:
            print e
    else:
        print(
            "Create Job %s" %
            jenkins_server.get_job_info(jenkins_jobname)['url'])
        jenkins_server.create_job(jenkins_jobname, jenkins_config)


def build_jenkins_jobs(options):
    # Connect to Jenkins CI server
    jenkins_server = jenkins.Jenkins(
        options['hostname'],
        options['username'],
        options['password'])
    jenkins_jobname = options['jobname']
    if jenkins_server.job_exists(jenkins_jobname):
        print(
            "Build Job %s" %
            jenkins_server.get_job_info(jenkins_jobname)['url'])
        try:
            jenkins_server.build_job(jenkins_jobname)
        except jenkins.JenkinsException, e:
            print e
