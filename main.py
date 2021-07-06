import falcon
import logs
from datetime import datetime
from database import Use, DBConnection
from middleware import CORSComponent
import csv
import pyotp

totp = pyotp.TOTP('DKEIR5BYLXTECP7BLI2C4WIUPKGFOAGE')

logger = logs.loguru_logger()


class DownloadCSV:
    class PseudoTextStream:
        def __init__(self):
            self.clear()

        def clear(self):
            self.result = []

        def write(self, data):
            self.result.append(data.encode())

    @logger.catch
    def data_generator(self, start_time, end_time):
        stream = self.PseudoTextStream()
        writer = csv.writer(stream, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(('上课时间', '课程节次', '任课老师', '班级', '计划人数', '实际人数', '设备状态'))
        start_time = datetime.strptime(start_time, "%Y-%m-%d").date if start_time else datetime.strptime("2000-01-01",
                                                                                                         "%Y-%m-%d").date
        end_time = datetime.strptime(start_time, "%Y-%m-%d").date if end_time else datetime.now().date
        nextPage = True
        page = 1
        offset = 100
        while nextPage:
            with DBConnection() as session:
                result = session.query(Use).filter(Use.userTime <= end_time, Use.userTime >= start_time).limit(
                    offset).offset((page - 1) * offset)
                print(result.count())
                for data in result:
                    writer.writerow((data.userTime.strftime("%Y-%m-%d %H:%M:%S"), data.classTime, data.teacherName,
                                     data.className, data.studentNumber, data.studentNum, data.status))
                    yield from stream.result
                    stream.clear()
                if result.count() != offset:
                    nextPage = False

    @logger.catch
    def on_get(self, req, resp):
        start_time = req.get_param('start_time', None)
        end_time = req.get_param('end_time', None)
        screct = req.get_param('screct', '')
        if not screct or not totp.verify(screct):
            resp.media = {'msg': "没有找到验证码或验证码不正确"}
            resp.status = falcon.HTTP_BAD_REQUEST
            return resp
        resp.content_type = 'text/csv'
        resp.downloadable_as = 'report.csv'
        resp.stream = self.data_generator(start_time, end_time)
        return resp


class FormData:
    @logger.catch
    def on_post(self, req, resp):
        className = req.media.get('classname', '')
        teacherName = req.media.get('teacher_name', '')
        studentNum = req.media.get('student_num', 0)
        studentNumber = req.media.get('stu_num', 0)
        status = req.media.get('status', '')
        use_time = req.media.get('use_time', '')
        class_time = req.media.get('class_time', '')
        if not (className and teacherName and use_time and class_time):
            resp.media = {'msg': "classname、teacher_name、use_time、class_time必须传值"}
            resp.status = falcon.HTTP_BAD_REQUEST
            return resp
        elif '、' not in class_time or not all([x.isdigit() for x in use_time.split('、')]):
            resp.media = {'msg': "class_time格式错误"}
            resp.status = falcon.HTTP_BAD_REQUEST
            return resp
        new_data = Use(
            teacherName=teacherName,
            className=className,
            studentNum=studentNum,
            studentNumber=studentNumber,
            status=status,
            userTime=datetime.strptime(use_time, "%Y-%m-%d %H:%M:%S").date if use_time else datetime.now().date,
            classTime=class_time
        )
        with DBConnection() as session:
            session.add(new_data)
            session.commit()
        resp.media = {"msg": "success"}
        return resp


api = falcon.App(
    middleware=[CORSComponent()], independent_middleware=True
)

api.add_route('/data', FormData())
api.add_route('/download', DownloadCSV())
