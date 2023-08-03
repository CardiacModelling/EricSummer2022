import nevis
from functools import wraps

from .result import Result

f = nevis.linear_interpolant()
f_grad = nevis.linear_interpolant(grad=True)


def optimizer(opt):
    """
    Decorator for optimization algorithms.

    Parameters
    ----------
    opt : function
        The optimization algorithm to decorate. The function should have the
        following signature:

        def opt(f, x_max, y_max, **kwargs):
            # MINIMIZE f((x, y)) subject to 0 <= x <= x_max and 0 <= y <= y_max
            # f(u, grad=None) returns the function value at u, and modifies
            # grad in place if grad is not None (as used in nlopt)
            # kwargs contains the hyper-parameters of the algorithm
            return {
                'x': (x_best, y_best),
                'z': z_best,
                'message': 'A message', # optional
                'trajectory': [(x, y), ...], # optional
                'ret_obj': ret_obj, # optional
            }

    Returns
    -------
    function, which can be used in the constructor of ``Algorithm``
    """

    @wraps(opt)
    def func(**params):
        points = []
        function_values = []

        def wrapper(u, grad=None):
            x, y = u
            points.append((x, y))
            if grad is not None and grad.size > 0:
                z, (gx, gy) = f_grad(x, y)
                grad[0] = gx
                grad[1] = gy
            else:
                z = f(x, y)
            function_values.append(z)
            return -z

        x_max, y_max = nevis.dimensions()

        res_dict = opt(
            wrapper,
            x_max,
            y_max,
            **params
        )

        x = res_dict['x']
        z = res_dict['z']
        message = res_dict.get('message', '')
        trajectory = res_dict.get('trajectory', [])
        ret_obj = res_dict.get('ret_obj')

        return Result(
            x,
            -z,
            points,
            message,
            function_values,
            trajectory=trajectory,
            ret_obj=ret_obj
        )
    return func
