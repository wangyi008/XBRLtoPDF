#! /usr/bin/env python
# encoding: utf-8

import re
#from marshmallow import Schema, fields
import datetime
import collections
import six
import logging

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

if 'OrderedDict' in dir(collections):
    odict = collections
else:
    import ordereddict as odict


def soup_maker(fh):
    """ Takes a file handler returns BeautifulSoup"""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(fh, "lxml")
        for tag in soup.find_all():
            tag.name = tag.name.lower()
    except ImportError:
        from BeautifulSoup import BeautifulStoneSoup
        soup = BeautifulStoneSoup(fh)
    return soup


class XBRLFile(object):
    def __init__(self, fh):
        """
        fh should be a seekable file-like byte stream object
        """
        self.headers = odict.OrderedDict()
        self.fh = fh


class XBRLParserException(Exception):
    pass


class XBRLParser(object):

    def __init__(self, precision=0):
        self.precision = precision

    @classmethod
    def parse(self, file_handle):
        """
        parse is the main entry point for an XBRLParser. It takes a file
        handle.
        """

        xbrl_obj = XBRL()

        # if no file handle was given create our own
        if not hasattr(file_handle, 'read'):
            file_handler = open(file_handle)
        else:
            file_handler = file_handle

        # Store the headers
        xbrl_file = XBRLPreprocessedFile(file_handler)

        xbrl = soup_maker(xbrl_file.fh)
        file_handler.close()
        xbrl_base = xbrl.find(name=re.compile("xbrl*:*"))

        if xbrl.find('xbrl') is None and xbrl_base is None:
            raise XBRLParserException('The xbrl file is empty!')

        # lookahead to see if we need a custom leading element
        lookahead = xbrl.find(name=re.compile("context",
                              re.IGNORECASE | re.MULTILINE)).name
        if ":" in lookahead:
            self.xbrl_base = lookahead.split(":")[0] + ":"
        else:
            self.xbrl_base = ""

        return xbrl











    @classmethod
    def MethodGenericList(self,
                    xbrl,
                    ignore_errors=0):
        """
        Parse company custom entities from XBRL and return an Custom object.
        """

        custom_data = xbrl.find_all(re.compile("(iic-com:IndiceRotacionCartera)",
            re.IGNORECASE | re.MULTILINE))

        elements = []
        for data in custom_data:
                element ={
                    'data_name_complete':data.name,
                    'data_name':data.name.split(':')[1],
                    'datatext':data.text
                }
                elements.append(element)

        return elements

    @classmethod
    def RegistroCNMV(self,
                    xbrl,
                    ignore_errors=0):
        """
        Parse company custom entities from XBRL and return an Custom object.
        """
        custom_obj = Custom()
        custom_data = xbrl.find_all(re.compile("(iic-com:RegistroCNMV)",
            re.IGNORECASE | re.MULTILINE))

        elements = []
        for data in custom_data:
                element ={
                    'data_name_complete':data.name,
                    'data_name':data.name.split(':')[1],
                    'datatext':data.text
                }
                elements.append(element)
        return elements

    @classmethod
    def AnoInforme(self,
                    xbrl,
                    ignore_errors=0):
        """
        Parse company custom entities from XBRL and return an Custom object.
        """
        custom_obj = Custom()
        custom_data = xbrl.find_all(re.compile("(iic-com:AnoInforme)",
            re.IGNORECASE | re.MULTILINE))

        elements = []
        for data in custom_data:
                element ={
                    'data_name_complete':data.name,
                    'data_name':data.name.split(':')[1],
                    'datatext':data.text
                }
                elements.append(element)
        return elements

    @classmethod
    def FondoCompartimentos(self,
                    xbrl,
                    ignore_errors=0):
        """
        Parse company custom entities from XBRL and return an Custom object.
        """
        custom_obj = Custom()
        custom_data = xbrl.find_all(re.compile("(iic-com-fon:FondoCompartimentos)",
            re.IGNORECASE | re.MULTILINE))

        elements = []
        for data in custom_data:
                element ={
                    'data_name_complete':data.name,
                    'data_name':data.name.split(':')[1],
                    'datatext':data.text
                }
                elements.append(element)
        return elements
    @classmethod
    def RatingDepositario(self,
                    xbrl,
                    ignore_errors=0):
        """
        Parse company custom entities from XBRL and return an Custom object.
        """
        custom_obj = Custom()
        custom_data = xbrl.find_all(re.compile("(iic-com:RatingDepositario)",
            re.IGNORECASE | re.MULTILINE))

        elements = []
        for data in custom_data:
                element ={
                    'data_name_complete':data.name,
                    'data_name':data.name.split(':')[1],
                    'datatext':data.text
                }
                elements.append(element)
        return elements


    @classmethod
    def MethodBolean(self,
                    xbrl,
                    data_name,
                    ignore_errors=0
                     ):
        """
        Parse company custom entities from XBRL and return an Custom object.
        """
        custom_data = xbrl.find_all(re.compile(data_name,
            re.IGNORECASE | re.MULTILINE))
        elements = []
        for data in custom_data:
                element ={
                    'data_name_complete':data.name,
                    'data_name':data.name.split(':')[1],
                    'datatext':data.text
                }
                elements.append(element)
        if elements[0]['datatext']=='true':
            return 'SI'
        else:
            return 'NO'

    @classmethod
    def MethodGeneric(self,
                    xbrl,
                    data_name,
                    ignore_errors=0
                     ):
        """
        Parse company custom entities from XBRL and return an Custom object.
        """
        custom_data = xbrl.find_all(re.compile(data_name,
            re.IGNORECASE | re.MULTILINE))
        elements = []
        for data in custom_data:
                element ={
                    'data_name_complete':data.name,
                    'data_name':data.name.split(':')[1],
                    'datatext':data.text
                }
                elements.append(element)
        return elements[0]['datatext']

    @classmethod
    def Prueba(self,
                    xbrl,
                    ignore_errors=0):
        """
        Parse company custom entities from XBRL and return an Custom object.
        """
        custom_data = xbrl.find_all(re.compile('(id="label_XCode_VocacionInversoraFIC_01")',
            re.IGNORECASE | re.MULTILINE))

        elements = []
        for data in custom_data:
                element ={
                    'data_name_complete':data.name,
                    'data_name':data.name.split(':')[1],
                    'datatext':data.text
                }
                elements.append(element)
        return elements



    @staticmethod
    def trim_decimals(s, precision=-3):
        """
        Convert from scientific notation using precision
        """
        encoded = s.encode('ascii', 'ignore')
        str_val = ""
        if six.PY3:
            str_val = str(encoded, encoding='ascii', errors='ignore')[:precision]
        else:
            # If precision is 0, this must be handled seperately
            if precision == 0:
                str_val = str(encoded)
            else:
                str_val = str(encoded)[:precision]
        if len(str_val) > 0:
            return float(str_val)
        else:
            return 0

    @staticmethod
    def is_number(s):
        """
        Test if value is numeric
        """
        try:
            s = float(s)
            return True
        except ValueError:
            return False

    @classmethod
    def data_processing(self,
                        elements,
                        xbrl,
                        ignore_errors,
                        logger,
                        context_ids=[],
                        **kwargs):
        """
        Process a XBRL tag object and extract the correct value as
        stated by the context.
        """
        options = kwargs.get('options', {'type': 'Number',
                                         'no_context': False})

        if options['type'] == 'String':
            if len(elements) > 0:
                    return elements[0].text

        if options['no_context'] == True:
            if len(elements) > 0 and XBRLParser().is_number(elements[0].text):
                    return elements[0].text

        try:

            # Extract the correct values by context
            correct_elements = []
            for element in elements:
                std = element.attrs['contextref']
                if std in context_ids:
                    correct_elements.append(element)
            elements = correct_elements

            if len(elements) > 0 and XBRLParser().is_number(elements[0].text):
                decimals = elements[0].attrs['decimals']
                if decimals is not None:
                    attr_precision = decimals
                    if xbrl.precision != 0 \
                    and xbrl.precison != attr_precision:
                        xbrl.precision = attr_precision
                if elements:
                    return XBRLParser().trim_decimals(elements[0].text,
                        int(xbrl.precision))
                else:
                    return 0
            else:
                return 0
        except Exception as e:
            if ignore_errors == 0:
                raise XBRLParserException('value extraction error')
            elif ignore_errors == 1:
                return 0
            elif ignore_errors == 2:
                logger.error(str(e) + " error at " +
                    ''.join(elements[0].text))


# Preprocessing to fix broken XML
# TODO - Run tests to see if other XML processing errors can occur
class XBRLPreprocessedFile(XBRLFile):
    def __init__(self, fh):
        super(XBRLPreprocessedFile, self).__init__(fh)

        if self.fh is None:
            return

        xbrl_string = self.fh.read()

        # find all closing tags as hints
        closing_tags = [t.upper() for t in re.findall(r'(?i)</([a-z0-9_\.]+)>',
                        xbrl_string)]

        # close all tags that don't have closing tags and
        # leave all other data intact
        last_open_tag = None
        tokens = re.split(r'(?i)(</?[a-z0-9_\.]+>)', xbrl_string)
        new_fh = StringIO()
        for idx, token in enumerate(tokens):
            is_closing_tag = token.startswith('</')
            is_processing_tag = token.startswith('<?')
            is_cdata = token.startswith('<!')
            is_tag = token.startswith('<') and not is_cdata
            is_open_tag = is_tag and not is_closing_tag \
                and not is_processing_tag
            if is_tag:
                if last_open_tag is not None:
                    new_fh.write("</%s>" % last_open_tag)
                    last_open_tag = None
            if is_open_tag:
                tag_name = re.findall(r'(?i)<*>', token)[0]
                if tag_name.upper() not in closing_tags:
                    last_open_tag = tag_name
            new_fh.write(token)
        new_fh.seek(0)
        self.fh = new_fh


class XBRL(object):
    def __str__(self):
        return ""





# Base Custom object
class Custom(object):

    def __init__(self):
        return None

    def __call__(self):
        return self.__dict__.items()
