# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from typing import Any, Callable, Iterable

from google.cloud.kms_v1.types import resources
from google.cloud.kms_v1.types import service


class ListKeyRingsPager:
    """A pager for iterating through ``list_key_rings`` requests.

    This class thinly wraps an initial
    :class:`~.service.ListKeyRingsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``key_rings`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListKeyRings`` requests and continue to iterate
    through the ``key_rings`` field on the
    corresponding responses.

    All the usual :class:`~.service.ListKeyRingsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[[service.ListKeyRingsRequest],
                service.ListKeyRingsResponse],
            request: service.ListKeyRingsRequest,
            response: service.ListKeyRingsResponse):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.service.ListKeyRingsRequest`):
                The initial request object.
            response (:class:`~.service.ListKeyRingsResponse`):
                The initial response object.
        """
        self._method = method
        self._request = service.ListKeyRingsRequest(request)
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[service.ListKeyRingsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)
            yield self._response

    def __iter__(self) -> Iterable[resources.KeyRing]:
        for page in self.pages:
            yield from page.key_rings

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListCryptoKeysPager:
    """A pager for iterating through ``list_crypto_keys`` requests.

    This class thinly wraps an initial
    :class:`~.service.ListCryptoKeysResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``crypto_keys`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListCryptoKeys`` requests and continue to iterate
    through the ``crypto_keys`` field on the
    corresponding responses.

    All the usual :class:`~.service.ListCryptoKeysResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[[service.ListCryptoKeysRequest],
                service.ListCryptoKeysResponse],
            request: service.ListCryptoKeysRequest,
            response: service.ListCryptoKeysResponse):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.service.ListCryptoKeysRequest`):
                The initial request object.
            response (:class:`~.service.ListCryptoKeysResponse`):
                The initial response object.
        """
        self._method = method
        self._request = service.ListCryptoKeysRequest(request)
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[service.ListCryptoKeysResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)
            yield self._response

    def __iter__(self) -> Iterable[resources.CryptoKey]:
        for page in self.pages:
            yield from page.crypto_keys

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListCryptoKeyVersionsPager:
    """A pager for iterating through ``list_crypto_key_versions`` requests.

    This class thinly wraps an initial
    :class:`~.service.ListCryptoKeyVersionsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``crypto_key_versions`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListCryptoKeyVersions`` requests and continue to iterate
    through the ``crypto_key_versions`` field on the
    corresponding responses.

    All the usual :class:`~.service.ListCryptoKeyVersionsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[[service.ListCryptoKeyVersionsRequest],
                service.ListCryptoKeyVersionsResponse],
            request: service.ListCryptoKeyVersionsRequest,
            response: service.ListCryptoKeyVersionsResponse):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.service.ListCryptoKeyVersionsRequest`):
                The initial request object.
            response (:class:`~.service.ListCryptoKeyVersionsResponse`):
                The initial response object.
        """
        self._method = method
        self._request = service.ListCryptoKeyVersionsRequest(request)
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[service.ListCryptoKeyVersionsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)
            yield self._response

    def __iter__(self) -> Iterable[resources.CryptoKeyVersion]:
        for page in self.pages:
            yield from page.crypto_key_versions

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)


class ListImportJobsPager:
    """A pager for iterating through ``list_import_jobs`` requests.

    This class thinly wraps an initial
    :class:`~.service.ListImportJobsResponse` object, and
    provides an ``__iter__`` method to iterate through its
    ``import_jobs`` field.

    If there are more pages, the ``__iter__`` method will make additional
    ``ListImportJobs`` requests and continue to iterate
    through the ``import_jobs`` field on the
    corresponding responses.

    All the usual :class:`~.service.ListImportJobsResponse`
    attributes are available on the pager. If multiple requests are made, only
    the most recent response is retained, and thus used for attribute lookup.
    """
    def __init__(self,
            method: Callable[[service.ListImportJobsRequest],
                service.ListImportJobsResponse],
            request: service.ListImportJobsRequest,
            response: service.ListImportJobsResponse):
        """Instantiate the pager.

        Args:
            method (Callable): The method that was originally called, and
                which instantiated this pager.
            request (:class:`~.service.ListImportJobsRequest`):
                The initial request object.
            response (:class:`~.service.ListImportJobsResponse`):
                The initial response object.
        """
        self._method = method
        self._request = service.ListImportJobsRequest(request)
        self._response = response

    def __getattr__(self, name: str) -> Any:
        return getattr(self._response, name)

    @property
    def pages(self) -> Iterable[service.ListImportJobsResponse]:
        yield self._response
        while self._response.next_page_token:
            self._request.page_token = self._response.next_page_token
            self._response = self._method(self._request)
            yield self._response

    def __iter__(self) -> Iterable[resources.ImportJob]:
        for page in self.pages:
            yield from page.import_jobs

    def __repr__(self) -> str:
        return '{0}<{1!r}>'.format(self.__class__.__name__, self._response)
