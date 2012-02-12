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

        if 'hostname' not in self.options:
            raise UserError(
                'Please provide a "hostname" in your jenkins section "%s"' %
                self.options['recipe'])
        if 'jobname' not in self.options:
            raise UserError(
                'Please provide a  "jobname" in your jenkins section "%s"' %
                self.options['recipe'])

        self.options.setdefault('port', '80')
        self.options.setdefault(
            'template',
            os.path.join(os.path.dirname(__file__),
            'default_config.xml.in'))
        self.options.setdefault('config_name', 'jenkins_config.xml')
        self.options.setdefault('username', '')
        self.options.setdefault('password', '')

        # figure out default output file
        plone_jenkins = os.path.join(
            self.buildout['buildout']['parts-directory'], __name__)
        if not os.path.exists(plone_jenkins):
            os.makedirs(plone_jenkins)

        # setup input/output file
        self.options['input'] = self.options['template']
        self.options['output'] = os.path.join(
            plone_jenkins,
            self.options['config_name'])

        # what files are tracked by this recipe
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
    jenkins_url = "http://jenkins.timostollenwerk.net/jenkins"
    jenkins_username = "timo"
    jenkins_password = ""
    jenkins_jobname = "plone.app.discussion"
    jenkins_config = open("jenkins.xml").read()

    # Connect to Jenkins CI server
    jenkins_server = jenkins.Jenkins(
        jenkins_url,
        jenkins_username,
        jenkins_password)

    # Create Jenkins job
    if jenkins_server.job_exists(jenkins_jobname):
        print("Reconfig Job %s" % jenkins_jobname)
        try:
            jenkins_server.reconfig_job(jenkins_jobname, jenkins_config)
        except jenkins.JenkinsException, e:
            print e
    else:
        print("Create Job %s" % jenkins_jobname)
        jenkins_server.create_job(jenkins_jobname, jenkins_config)
