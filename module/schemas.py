from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Str()
    name = fields.Str()

class CategorySchema(Schema):
    id = fields.Str()
    category_name = fields.Str()

class RecordSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    category_id = fields.Int(required=True)
    timestamp = fields.DateTime(dump_only=True)
    amount = fields.Float(required=True)