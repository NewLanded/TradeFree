from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from conf import DB_CONNECT

engine = create_engine(DB_CONNECT, echo=False, pool_size=10, pool_recycle=3600)
DBSession = sessionmaker(bind=engine)


def get_connection():
    session = DBSession()
    return session


def assem_sql(keyword, condition_list, args, default_value="null"):
    """
    将condition_list中的值拼装为sql中in关键字可以使用的
    :param keyword:  xxx
    :param condition_list: ['a', 'b']
    :param args:  {}
    :return:
        "xxx_0, xxx_1"

        {
            xxx_0: 'a',
            xxx_1: 'b'
        }
    """
    if not condition_list:
        return default_value

    keyword_str_list = []
    for index, condition_value in enumerate(condition_list):
        args[keyword + "_" + str(index)] = condition_value
        keyword_str_list.append(keyword + "_" + str(index))
    keyword_str = ",".join(keyword_str_list)
    return keyword_str


def get_multi_data(session, sql, args=None):
    try:
        if args is None:
            result = session.execute(sql).fetchall()
        else:
            result = session.execute(sql, args).fetchall()
    except Exception as e:
        raise e

    return result


def get_single_column(session, sql, args=None):
    result = get_multi_data(session, sql, args)
    result = [i[0] for i in result]
    return result


def get_single_row(session, sql, args=None):
    try:
        if args is None:
            result = session.execute(sql).first()
        else:
            result = session.execute(sql, args).first()
    except Exception as e:
        raise e

    return result


def get_single_value(session, sql, args=None):
    result = get_multi_data(session, sql, args)
    result = None if not result else result[0][0]
    return result


def get_boolean_value(session, sql, args=None):
    result = get_multi_data(session, sql, args)
    if len(result) > 0 and result[0][0] == 1:
        return True
    else:
        return False


def update_data(session, sql, args=None):
    try:
        if args is None:
            session.execute(sql)
        else:
            session.execute(sql, args)
        session.commit()
    except Exception as e:
        raise e
