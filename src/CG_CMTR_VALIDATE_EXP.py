# AUTOSCRIPT NAME: CG_CMTR_VALIDATE_EXP
# CREATEDDATE: 2012-04-21 16:36:28
# CREATEDBY: UFQJ
# CHANGEDATE: 2013-08-28 08:20:59
# CHANGEBY: UFDA
# SCRIPTLANGUAGE: jython
# STATUS: Draft

from psdi.common.expbuilder import ExpressionBuilderFormat

objName = mbo.getString("expobject")
expression = mbo.getString("condition")

if expression is not None :
    ebf = ExpressionBuilderFormat(mbo,objName)
    ebf.validate(expression,ExpressionBuilderFormat.VALIDATE_THROW_SQLEXCEPTION)