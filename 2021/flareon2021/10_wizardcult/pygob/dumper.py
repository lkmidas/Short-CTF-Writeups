import io

from .types import (BOOL, INT, UINT, FLOAT, BYTE_SLICE, STRING, COMPLEX,
                    WIRE_TYPE, ARRAY_TYPE, COMMON_TYPE, SLICE_TYPE,
                    STRUCT_TYPE, FIELD_TYPE, FIELD_TYPE_SLICE, MAP_TYPE)
from .types import (GoBool, GoInt, GoUint, GoFloat, GoStruct, GoByteSlice,
                    GoString, GoComplex)


class Dumper:
    def __init__(self):
        common_type = GoStruct(COMMON_TYPE, 'CommonType', self, None, [
            ('Name', STRING),
            ('Id', INT),
        ])
        self.types = {
            bool: GoBool,
            int: GoInt,
            float: GoFloat,
            bytes: GoByteSlice,
            str: GoString,
            complex: GoComplex,
        }
        self.nextId = 64 # type Id start from 65
        self.idToType = {
            COMMON_TYPE: common_type
        }

    def setTypeId(self, typ):
        if typ.typeId() != 0 :
            return
        self.nextId += 1
        typ.setId(self.nextId)
        self.idToType[self.nextId] = typ

    def newArrayType(self):
        typ = GoStruct(ARRAY_TYPE, 'ArrayType', None, self, [
            ('CommonType', COMMON_TYPE),
            ('Elem', INT),
            ('Len', INT),
        ])
        return typ

    def newMapType(self):
        typ = GoStruct(MAP_TYPE, 'MapType', None, self, [
            ('CommonType', COMMON_TYPE),
            ('Key', INT),
            ('Elem', INT),
        ])
        return typ

    def newStructType(self, name):
        typ = GoStruct(0, name, None, self, [])
        self.setTypeId(typ)
        return typ

    def newTypeObj(self, value):
        python_type = type(value)
        go_type = self.types.get(python_type)
        if go_type is not None:
            return go_type

        if python_type == list:
            go_type = self.newArrayType()
        elif python_type == dict:
            go_type = self.newMapType()
        elif python_type == tuple:
            return None
        else:
            go_type = self.newStructType(python_type.__name__)
            fields = []
            if hasattr(value, '__dict__'):
                fields = value.__dict__.keys()
            else:
                fields = value._fields
            for field in fields:
                gt = self.getType(getattr(value, field))
                go_type._fields.append((field, gt.typeid))

        self.types[python_type] = go_type
        self.idToType[go_type.typeId()] = go_type
        return go_type

    def getType(self, value):
        python_type = type(value)
        go_type = self.types.get(python_type)
        if go_type is not None:
            return go_type
        return self.newTypeObj(value)

    def dump(self, value):
        return self._dump(value)

    def _dump(self, value):
        # Top-level singletons are sent with an extra zero byte which
        # serves as a kind of field delta.
        go_type = self.getType(value)
        if go_type is None:
            raise NotImplementedError("cannot encode %s of type %s" %
                                      (value, python_type))

        segment = io.BytesIO()
        segment.write(GoInt.encode(go_type.typeid))
        print(go_type)
        if not isinstance(go_type, GoStruct):
            segment.write(b'\x00')
        segment.write(go_type.encode(value))
        return GoUint.encode(segment.tell()) + segment.getvalue()
