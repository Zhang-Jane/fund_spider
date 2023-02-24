import datetime
import json

dic = {
    'k1': 123,
    'ctime': datetime.datetime.now()
}


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d')
        else:
            return super(MyEncoder, self).default(o)


if __name__ == '__main__':
    print(dic)
    v = json.dumps(dic, cls=MyEncoder)
    print(type(v))
