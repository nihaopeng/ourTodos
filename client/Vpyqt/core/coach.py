
from core.LLMCaller import LLMCaller
from core.provider import deepseek
from PySide6.QtCore import QObject, Signal, QThread

class Step():
    def __init__(self,stepName) -> None:
        self.stepName = stepName

class genStepWorker(QObject):
    stepSignal = Signal(Step)   # 每次接收到的分块
    startSignal = Signal()
    finished = Signal()          # 完成信号
    errorSignal = Signal(str)

    def __init__(self, llmcaller, query):
        super().__init__()
        self.llmcaller = llmcaller
        self.query = query

    def run(self):
        buffer = ""
        try:
            for chunk in self.llmcaller.stream(self.query):
                self.startSignal.emit()
                buffer += chunk
                # 遇到换行，说明收集到一个完整 step
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if line:
                        step = Step(line)
                        self.stepSignal.emit(step)
            # 处理最后一行（可能没有换行）
            if buffer.strip():
                step = Step(buffer.strip())
                self.stepSignal.emit(step)
            self.finished.emit()
        except Exception as e:
            self.errorSignal.emit(str(e))


class CoachManager(QObject):
    stepSignal = Signal(Step)   # 每次接收到的分块
    startSignal = Signal()
    finishSignal = Signal()          # 完成信号
    errorSignal = Signal(str)
    def __init__(self) -> None:
        super().__init__()
        # 逻辑处理
        self.LLMCaller = LLMCaller()  # 假设你有一个 LLMCaller 类来处理模型调用
        self.LLMCaller.register_model("deepseek", deepseek.handler_factory)

    def genStep(self,task):
        TEMPLATE = """
        现在有一个用户的任务，但是处于某些原因，用户没有动力完成这个任务。
        你需要充当一个教练，根据用户现在所处的状态，帮助用户完成这个任务。
        请将任务分解为多个步骤
        每个步骤一行,只输出步骤
        注意重点是如何启动这个任务，而不是如何完成这个任务，比如：我说我现在躺在床上玩手机，想去自习室学习
        你可以提出
        1、起身，离开床铺
        2、穿鞋
        3、带上学习用品
        4、前往自习室
        可以细致一些，不要太宽泛。

        任务如下：
        <task>
        {task}
        </task>
        """.format(task=task)
        # 创建 worker + 线程
        self.thread = QThread()
        self.worker = genStepWorker(self.LLMCaller, TEMPLATE)
        self.worker.moveToThread(self.thread)
        # 连接信号
        self.thread.started.connect(self.worker.run)
        self.worker.stepSignal.connect(self.stepSignal.emit)
        self.worker.startSignal.connect(self.startSignal.emit)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # 启动线程
        self.thread.start()
        
