# -*- coding: utf-8 -*-
"""Recipe jenkinsjob"""
import os
import sys
import urllib2

import zc.recipe.egg
from zc.buildout import UserError
from collective.recipe.template.genshitemplate import Recipe as GenshiRecipe


class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options
        self.egg = zc.recipe.egg.Scripts(
            buildout,
            self.options['recipe'],
            options)

        if 'host' not in self.options:
            raise UserError(
                'Please provide a "host" in your jenkins section "%s"' %
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
        # generate script create_jenkins_job
        zc.buildout.easy_install.scripts(
            [(self.name, 'collective.recipe.jenkinsjob', 'create_jenkins_job')],
            self.egg.working_set()[1],
            self.buildout[self.buildout['buildout']['python']]['executable'],
            self.buildout['buildout']['bin-directory'],
            arguments=self.options.__repr__(),
        )

    def render_jenkins_config(self):
        """render our jenkins template"""
        g = GenshiRecipe(self.buildout, self.name, self.options)
        g.install()


def create_jenkins_job(options):
    """Makes HTTP POST request to jenkins to add new job.

    :param options: Configuration to jenkins instance
    :type options: dict

    """
    host = "http://%(host)s:%(port)s/createItem?name=%(jobname)s" % options
    headers = {
        "Content-Type": "application/xml; charset=utf-8",
    }
    opener = urllib2.build_opener()
    if options.get('username', None):
        auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password(
            realm='Jenkins',
            uri=host,
            user=options['username'],
            passwd=options['password'])
        opener.add_handler(auth_handler)

    # upload jenkins config
    params = open(options['output']).read()
    try:
        print "Creating new job at %s" % host
        opener.open(urllib2.Request(host, params, headers))
    except urllib2.HTTPError as e:
        print e
        print "\t(does the job maybe already exists?)"
        sys.exit(2)
    else:
        print "Done."
