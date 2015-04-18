__author__ = 'evanwu'
from configparser import ConfigParser

def read_db_config(filename='python_mysql/config.ini', section='mysql'):
    """
    Read database configuration file and return a dictionary
    :param filename: name of the configuration
    :param section: section of database configuration
    :return: A dictionary of database parameters
    """

    # Create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {} #initialize the dictionary
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db