from app import app, db
from app.model import User, Storage, Host, OperationSystem, RigConnection, Rig, HostUsage
import os

from werkzeug.security import generate_password_hash

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = '../data/spe_djy_lab.sqlite'
# this is for sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
# this is for mysql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@Baidu123@localhost:3306/test'
app.config['SQLALCHEMY_ECHO'] = True


def drop_db():
    db.drop_all()


def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    db.drop_all()
    db.create_all()
    # passwords are hashed, to use plaintext passwords instead:
    # test_user = User(login="test", password="test")
    test_user = User(login="yangreid", password=generate_password_hash("yangtao159"))
    db.session.add(test_user)

    for temp in ['Unity', 'Rockies', 'VSA', 'VNXe3200']:
        storage = Storage()
        storage.name = temp
        db.session.add(storage)

    for temp in ['Linux', 'Windows', 'ESXi', 'vCenter']:
        operation_system = OperationSystem()
        operation_system.name = temp
        db.session.add(operation_system)

    for temp in ['FC', 'CIFS', 'NFS', 'ISCSI', 'VMWARE', 'Command']:
        host_usage = HostUsage()
        host_usage.name = temp
        db.session.add(host_usage)

    for temp in ['IMT', 'Metro-Sync', 'Async', 'SanCopy', 'Move']:
        rig_connect = RigConnection()
        rig_connect.name = temp
        db.session.add(rig_connect)

    for temp in ['10.109.80.121','10.109.143.181','10.109.140.167','10.109.82.56',
                    '10.109.82.168','10.109.140.113','10.244.128.114','10.244.128.115',
                     '10.141.56.216','10.109.143.184','10.109.82.132','10.141.56.188']:
        host = Host()
        host.ip = temp

        db.session.add(host)

    for temp in ['OB-D1468', 'OB-D1442', 'OB-D1499', 'OB-D1453', 'OB-D1462', 'OB-D1490', 'OB-D1476',
                 'OB-D1465', 'OB-D1434', 'OB-D1473', 'OB-D1464', 'OB-D1471', 'OB-D1489', 'OB-D1458',
                 'OB-D1436', 'OB-D1441', 'VD-D1192', 'VD-D1202']:
        rig = Rig()
        rig.name = temp
        db.session.add(rig)
    db.session.commit()

    return


if __name__ == '__main__':

    build_sample_db()
    # drop_db()
    # Start app
    #app.run(debug=True)
