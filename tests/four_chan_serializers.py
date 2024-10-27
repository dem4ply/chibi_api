from functools import reduce

from marshmallow import Schema, pre_load, INCLUDE, fields
from chibi_marshmallow.fields import Timestamp


class Reduce_threads( Schema ):
    @pre_load( pass_many=True )
    def reduce_threads( self, data, **kw ):
        threads = reduce(
            ( lambda x, y: x + y ),
            ( page[ 'threads' ] for page in data ) )
        return threads


class Thread( Reduce_threads ):
    id = fields.Integer( data_key='no' )
    replies = fields.Integer()
    last_modified = Timestamp()

    class Meta:
        unknown = INCLUDE


class Post( Schema ):
    id = fields.Integer( data_key='no' )
    created_at = Timestamp( data_key='time' )
    file_name = fields.String( data_key='filename' )
    comment = fields.String( data_key='com' )
    title = fields.String( data_key='sub' )

    class Meta:
        unknown = INCLUDE

    @pre_load( pass_many=True )
    def pre_load( self, data, **kw ):
        if 'posts' in data:
            return data.posts
        return data


class Catalog( Reduce_threads ):
    id = fields.Integer( data_key='no' )
    created_at = Timestamp( data_key='time' )
    last_replies = fields.Nested( Post, many=True )
    last_modified = Timestamp()
    title = fields.String( data_key='sub' )
    comment = fields.String( data_key='com' )

    class Meta:
        unknown = INCLUDE
