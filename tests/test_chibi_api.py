#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock

from chibi_requests import Response
from vcr_unittest import VCRTestCase

from chibi_api import Chibi_api
from chibi_api.chibi_api import Chibi_inner_api
from tests.four_chan_serializers import Catalog as Catalog_serializer


class Catalog( Response ):
    serializer = Catalog_serializer


class Four_chan_inner( Chibi_inner_api ):
    @property
    def json( self ):
        return self.add_subfix( '.json' )

    @property
    def catalog( self ):
        url = self._build_url( 'catalog', response_class=Catalog )
        return url


class Four_chan( Chibi_api ):
    schema = 'http'
    host = 'a.4cdn.org'
    inner_api_class = Four_chan_inner


class Test_chibi_inenr_api( unittest.TestCase ):
    def test_when_build_url_should_pass_response( self ):
        url = Chibi_inner_api()._build_url( "some_url", response_class=Mock )
        self.assertIs( url.response_class, Mock )


class Test_catalog_url( VCRTestCase ):
    def test_the_inner_api_should_be_chibi_api_inner( self ):
        result = Four_chan.API.catalog
        self.assertIsInstance( result, Chibi_inner_api )
        result = Four_chan.API.catalog.w
        self.assertIsInstance( result, Chibi_inner_api )

    def test_the_inner_should_work_as_expected( self ):
        result = Four_chan.API.catalog
        self.assertEqual( str( result ), 'http://a.4cdn.org/catalog' )
        result = Four_chan.API.catalog.w
        self.assertEqual( str( result ), 'http://a.4cdn.org/catalog/w' )

    def test_catalog_should_have_a_catalog_response( self ):
        catalog = Four_chan.API.w.catalog
        self.assertEqual( catalog.response_class, Catalog )

    def test_each_thread_should_have_a_url( self ):
        w = Four_chan.API.w.catalog
        url = w.json
        response = url.get()
        self.assertTrue( response.ok )

    def test_each_thread_should_have_a_title( self ):
        response = Four_chan.API.w.catalog.json.get()
        self.assertEqual( response.status_code, 200 )
        thread_with_title = list(
            thread for thread in response.native if 'title' in thread )
        self.assertTrue( thread_with_title )
        for thread in thread_with_title:
            self.assertIn( 'title', thread )
            self.assertTrue( thread.title )
