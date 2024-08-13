import re
from jsonschema import ValidationError


def immediateChardSchema():
    return {
        "type": "object",
        "properties": {
            "calendario": {
                "type": "object",
                "properties": {
                    "expiracao": {"type": "number", "maximum": 2147483647}
                }
            },
            "cpf": {"type": "string", "pattern": "^\d{11}$"},
            "cnpj": {"type": "string", "pattern": "^\d{14}$"},
            "nome": {"type": "string", "maxLength": 200},
            "loc": {
                "type": "object",
                "properties": {
                    "tipoCob": {"type": "string"}
                }
            },
            "valor": {
                "type": "object",
                "properties": {
                    "original": {"type": "string"},
                    "modalidadeAlteracao": {"type": "number"},
                    "retirada": {
                        "type": "object",
                        "properties": {
                            "saque": {
                                "type": "object",
                                "properties": {
                                    "valor": {"type": "string", "pattern": "\d{1,10}\.?\d{2}"},
                                    "modalidadeAlteracao": {"type": "number", "maxLength": 1, "minLength": 0},
                                    "modalidadeAgente": {"type": "string"},
                                    "prestadorDoServicoDeSaque": {"type": "string"},
                                }
                            },
                            "troco": {
                                "type": "object",
                                "properties": {
                                    "valor": {"type": "string", "pattern": "\d{1,10}\.?\d{2}"},
                                    "modalidadeAlteracao": {"type": "number"},
                                    "modalidadeAgente": {"type": "string"},
                                    "prestadorDoServicoDeSaque": {"type": "string"},
                                }
                            }
                        }
                    },
                }
            },
            "chave": {"type": "string", "maxLength": 77, "minLength": 1},
            "solicitacaoPagador": {"type": "string", "maxLength": 140, "minLength": 1},
            "infoAdicionais": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string", "maxLength": 200, "minLength": 1},
                    "valor": {"type": "string", "maxLength": 50, "minLength": 1}
                }
            }
        }
    }

def includePaymentPixSchema():
    return {
        "type": "object",
        "properties": {
            "valor": {"type": "string"},
            "descricao": {"type": "string"},
            "destinatario": {
                "type": "object",
                "properties":{
                    "tipo": {"type": "string"},
                    "chave": {"type": "string"}
                }
            },
        },
    }



def formatValue(value):
    if value.count(",") > 0:
        value = value.replace(".", "").replace(",", ".")
    if value.count(".") > 1:
        value = re.sub(r'\.(?=.*\.)', '', value)
    if not value or value == ".":
        return "00.00"
    if value.endswith("."):
        value += "00"
    elif value.startswith("."):
        if re.match("\.\d{1}$", value):
            value = "00" + value + "0"
        else:
            value = "00" + value
    elif "." not in value:
        value += ".00"
    elif re.match("^\d{1}(?:\.\d{1,1})?$", value):
        value = "0" + value + "0"
        # if re.match("\.\d{1}", value):
    elif value.count(".") == 1 and not value.startswith(".") and not value.endswith("."):
        parts = value.split(".")
        if len(parts[1]) == 1:
            parts[1] += "0"
        value = ".".join(parts)

    return value


def validateValue(value):
    if not re.match("^\d{0,10}(?:\.\d{1,2})?$", value):
        raise ValidationError("Invalid currency format: " + value)
    if not value or value == ".":
        raise ValidationError("Invalid currency value.")
    if not value or value == ".":
        raise ValidationError(
            "Value must not be Zero. Invalid currency value.")
    if float(value) == 0:
        raise ValidationError(
            "Value must not be Zero. Invalid currency value.")
