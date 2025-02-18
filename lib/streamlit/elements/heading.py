# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
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

from typing import TYPE_CHECKING, Optional, cast

from streamlit.proto.Heading_pb2 import Heading as HeadingProto
from streamlit.runtime.metrics_util import gather_metrics
from streamlit.string_util import clean_text
from streamlit.type_util import SupportsStr

if TYPE_CHECKING:
    from streamlit.delta_generator import DeltaGenerator


class HeadingMixin:
    @gather_metrics
    def header(
        self, body: SupportsStr, anchor: Optional[str] = None
    ) -> "DeltaGenerator":
        """Display text in header formatting.

        Parameters
        ----------
        body : str
            The text to display.

        anchor : str
            The anchor name of the header that can be accessed with #anchor
            in the URL. If omitted, it generates an anchor using the body.

        Example
        -------
        >>> st.header('This is a header')

        """
        header_proto = HeadingProto()
        if anchor is not None:
            header_proto.anchor = anchor
        header_proto.body = clean_text(body)
        header_proto.tag = "h2"
        return self.dg._enqueue("heading", header_proto)

    @gather_metrics
    def subheader(
        self, body: SupportsStr, anchor: Optional[str] = None
    ) -> "DeltaGenerator":
        """Display text in subheader formatting.

        Parameters
        ----------
        body : str
            The text to display.

        anchor : str
            The anchor name of the header that can be accessed with #anchor
            in the URL. If omitted, it generates an anchor using the body.

        Example
        -------
        >>> st.subheader('This is a subheader')

        """
        subheader_proto = HeadingProto()
        if anchor is not None:
            subheader_proto.anchor = anchor
        subheader_proto.body = clean_text(body)
        subheader_proto.tag = "h3"

        return self.dg._enqueue("heading", subheader_proto)

    @gather_metrics
    def title(
        self, body: SupportsStr, anchor: Optional[str] = None
    ) -> "DeltaGenerator":
        """Display text in title formatting.

        Each document should have a single `st.title()`, although this is not
        enforced.

        Parameters
        ----------
        body : str
            The text to display.

        anchor : str
            The anchor name of the header that can be accessed with #anchor
            in the URL. If omitted, it generates an anchor using the body.

        Example
        -------
        >>> st.title('This is a title')

        """
        title_proto = HeadingProto()
        if anchor is not None:
            title_proto.anchor = anchor
        title_proto.body = clean_text(body)
        title_proto.tag = "h1"

        return self.dg._enqueue("heading", title_proto)

    @property
    def dg(self) -> "DeltaGenerator":
        """Get our DeltaGenerator."""
        return cast("DeltaGenerator", self)
