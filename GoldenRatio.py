import Task as t


class GoldenRatioSolver:
    def __init__(self, task: t.Task):
        self.task = task
        self.func_call_count = 0
        self.phi = (1 + 5 ** 0.5) / 2

    def solve(self, eps, ye, pk):
        self.func_call_count = 2
        alpha = (3 - 5 ** 0.5)/2
        x_2 = self.task.b - alpha * (self.task.b - self.task.a)
        x_1 = self.task.a + alpha * (self.task.b - self.task.a)
        fx_1 = self.task.func(ye + x_1 * pk)
        fx_2 = self.task.func(ye + x_2 * pk)
        while abs(self.task.a - self.task.b) > eps:
            if fx_1 > fx_2:
                self.task.b = x_2
                x_2 = x_1
                fx_2 = fx_1
                x_1 = self.task.a + alpha * (self.task.b - self.task.a)
                self.func_call_count += 1
                fx_1 = self.task.func(ye + x_1 * pk)
            else:
                self.task.a = x_1
                x_1 = x_2
                fx_1 = fx_2
                x_2 = self.task.b - alpha * (self.task.b - self.task.a)
                self.func_call_count += 1
                fx_2 = self.task.func(ye + x_2 * pk)
        return (self.task.a + self.task.b) / 2