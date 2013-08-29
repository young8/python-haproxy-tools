"""
Copyright (C) 2013 - Aybuke Ozdemir <aybuke.147@gmail.com>

This file is part of python-haproxy-tools

python-haproxy-tools is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

python-haproxy-tools is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>

"""
from utils import *

class HAProxyConfig():

    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.readConfig()
        self.globalh = Global(self.__getSection('global'))
        self.defaults = Defaults(self.__getSection('global'))

        #Set Listen.
        self.listens = []
        for name in self.getSectionNames('listen'):
            l = Listen(self.__getSection('listen', name))
            self.listens.append(l)

        # Set Frontends.
        self.frontends = []
        for name in self.getSectionNames('frontend'):
            f = Frontend(self.__getSection('frontend', name))
            self.frontends.append(f)

        #Set Backend.
        self.backends = []
        for name in self.getSectionNames('backend'):
            b = Backend(self.__getSection('backend', name))
            self.backends.append(b)

    def __getSectionWithName(self, title, name):
        config_array = []
        title = title.strip()
        start_flag = False

        for line in self.config:
            line = line.strip()

            if line == '':
                continue

            line_array = line.split()
            ltitle = line_array[0].strip()

            if len(line_array)> 1:
                lname = line_array[1].strip()
            if ltitle == title.strip():
                if name == lname:
                    config_array.append(line)
                    start_flag = True
                    continue

            if ltitle in SECTIONS:
                start_flag = False

            if start_flag:
                config_array.append(line)
        return config_array

    def __getSection(self, title):


    def getFrontend(self, name=None):
        ca = self.__getSectionWithName('frontend', name)
        return ca

    def readConfig(self):
        config_file = open(self.config_path)
        config = config_file.readlines()
        config_file.close()
        return config

    def getSectionNames(self, title):
        l_names = []
        for row in self.config:
            row = row.strip()
            if row.startswith(title):
                name = row.split()[1]
                l_names.append(name )
        return l_names

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.readConfig()

class Option():
    def __init__(self, param_name, params):
        self.name = param_name
        self.params = params

    def getRow(self):
        return self.__repr__()

    def getParamName(self):
        return self.name

    def getParams(self):
        return self.params

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.name + " " + " ".join(self.params))


class Section():
    def __init__(self, config_array):
        self.config_array = config_array
        self.options = []
        self.description = None

        is_first_row = True
        for row in self.config_array:
            if is_first_row:
                is_first_row = False
                items = row.split()
                title = items[0]

                if len(items) > 1:
                    name = items[1]
                else:
                    name = None
                if len(items) > 2:
                    params = items[2:]
                else:
                    params = None

                self.description = Description(title, name, params)

                continue

            param_name = self.getParamName(row).strip()
            params = self.getParams(row)
            option = Option(param_name, params)
            self.options.append(option)

    def getParamName(self, row):
        return row.split()[0]

    def getParams(self, row):
        return tuple(row.split()[1:])

    def getConfig(self):
        opts = self.options
        des = self.description
        config_output = ""
        config_output += str(des) + '\n'
        for opt in opts:
            config_output += '    ' + str(opt) + '\n'
        return config_output

    def addOption(self, option):
        self.options.append(option)
        return True

    def delOption(self, option):
        for opt in self.options:
            if opt == option.name:
                self.options.remove(opt)
        return True
    def setOption(self, option):
        for opt in self.options:
            if opt.name == option.name:
                opt.params = option.params
        return self.options

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.getConfig()

class Description():
    def __init__(self, title, name=None, params=None):
        self.title = title
        self.name = name
        self.params = params

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        out = []
        out.append(self.title)
        if self.name:
            out.append(self.name)
        if self.params:
            out + self.params
        return " ".join(out)

class Global(Section):
    def __init__(self, config_array):
        print '### global'
        Section.__init__(self, config_array)

class Defaults(Section):
    def __init__(self, config_array):
        print '### defaults'
        Section.__init__(self, config_array)

class Listen(Section):
    def __init__(self, config_array):
        print '### listen'
        Section.__init__(self, config_array)

class Frontend(Section):
    def __init__(self, config_array):
        print '### frontend'
        Section.__init__(self, config_array)

class Backend(Section):
    def __init__(self, config_array):
        print '### backend'
        Section.__init__(self, config_array)

