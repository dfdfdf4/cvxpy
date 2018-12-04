from cvxpy.atoms.affine.add_expr import AddExpression
from cvxpy.atoms.affine.binary_operators import MulExpression, DivExpression, multiply
from cvxpy.atoms.affine.trace import trace
from cvxpy.atoms.elementwise.exp import exp
from cvxpy.atoms.elementwise.log import log
from cvxpy.atoms.elementwise.power import power
from cvxpy.atoms.elementwise.maximum import maximum
from cvxpy.atoms.geo_mean import geo_mean
from cvxpy.atoms.one_minus import one_minus
from cvxpy.atoms.eye_minus_inv import eye_minus_inv
from cvxpy.atoms.pnorm import pnorm
from cvxpy.atoms.sum_largest import sum_largest
from cvxpy.expressions.constants.constant import Constant
from cvxpy.expressions.variable import Variable
from cvxpy.reductions.eliminate_pwl.atom_canonicalizers import CANON_METHODS as PWL_METHODS
from cvxpy.reductions.gp2dcp.atom_canonicalizers.add_canon import add_canon
from cvxpy.reductions.gp2dcp.atom_canonicalizers.constant_canon import constant_canon
from cvxpy.reductions.gp2dcp.atom_canonicalizers.div_canon import div_canon
from cvxpy.reductions.gp2dcp.atom_canonicalizers.exp_canon import exp
from cvxpy.reductions.gp2dcp.atom_canonicalizers.eye_minus_inv_canon import eye_minus_inv_canon
from cvxpy.reductions.gp2dcp.atom_canonicalizers.geo_mean_canon import geo_mean_canon
from cvxpy.reductions.gp2dcp.atom_canonicalizers.log_canon import log_canon
from cvxpy.reductions.gp2dcp.atom_canonicalizers.mul_canon import mul_canon
from cvxpy.reductions.gp2dcp.atom_canonicalizers.mulexpression_canon import mulexpression_canon
from cvxpy.reductions.gp2dcp.atom_canonicalizers.nonpos_constr_canon import nonpos_constr_canon
from cvxpy.reductions.gp2dcp.atom_canonicalizers.one_minus_canon import one_minus_canon
from cvxpy.reductions.gp2dcp.atom_canonicalizers.pnorm_canon import pnorm_canon
from cvxpy.reductions.gp2dcp.atom_canonicalizers.power_canon import power_canon
from cvxpy.reductions.gp2dcp.atom_canonicalizers.trace_canon import trace_canon


# TODO(akshayka): canon for ...
#   sum_smallest,
#   minimum, (add a class and lower it to maximum in a canonicalizer)
#   cumsum,
CANON_METHODS = {
    AddExpression : add_canon,
    Constant : constant_canon,
    DivExpression : div_canon,
    exp : exp_canon,
    eye_minus_inv : eye_minus_inv_canon,
    geo_mean : geo_mean_canon,
    log : log_canon,
    MulExpression : mulexpression_canon,
    multiply : mul_canon,
    one_minus : one_minus_canon,
    pnorm : pnorm_canon,
    power : power_canon, 
    trace : trace_canon,
    Variable : None,
}

CANON_METHODS[maximum] = PWL_METHODS[maximum]
CANON_METHODS[sum_largest] = PWL_METHODS[sum_largest]

class DgpCanonMethods(dict):
    def __init__(self, *args, **kwargs):
        super(DgpCanonMethods, self).__init__(*args, **kwargs)
        self._variables = {}

    def __contains__(self, key):
        return key in CANON_METHODS

    def __getitem__(self, key):
        if key == Variable:
            return self.variable_canon
        else:
            return CANON_METHODS[key]

    def variable_canon(self, expr, args):
        # Swaps out positive variables for unconstrained variables.
        if expr in self._variables:
            return self._variables[expr], []
        else:
            log_variable =  Variable(expr.shape, var_id=expr.id)
            self._variables[expr] = log_variable
            return log_variable, []
