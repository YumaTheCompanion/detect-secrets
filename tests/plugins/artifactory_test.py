from __future__ import absolute_import

import pytest

from detect_secrets.plugins.artifactory import ArtifactoryDetector


class TestArtifactoryDetector(object):

    @pytest.mark.parametrize(
        'payload, should_flag',
        [
            ('AP6xxxxxxxxxx', True),
            ('AKCxxxxxxxxxx', True),
            (' AP6xxxxxxxxxx', True),
            (' AKCxxxxxxxxxx', True),
            ('=AP6xxxxxxxxxx', True),
            ('=AKCxxxxxxxxxx', True),
            ('\"AP6xxxxxxxxxx\"', True),
            ('\"AKCxxxxxxxxxx\"', True),
            ('artif-key:AP6xxxxxxxxxx', True),
            ('artif-key:AKCxxxxxxxxxx', True),
            ('X-JFrog-Art-Api: AKCxxxxxxxxxx', True),
            ('X-JFrog-Art-Api: AP6xxxxxxxxxx', True),
            ('artifactoryx:_password=AKCxxxxxxxxxx', True),
            ('artifactoryx:_password=AP6xxxxxxxxxx', True),
            ('testAKCwithinsomeirrelevantstring', False),
            ('testAP6withinsomeirrelevantstring', False),
            ('X-JFrog-Art-Api: $API_KEY', False),
            ('X-JFrog-Art-Api: $PASSWORD', False),
            ('artifactory:_password=AP6xxxxxxxx', False),
            ('artifactory:_password=AKCxxxxxxxx', False),
        ],
    )
    def test_analyze_string(self, payload, should_flag):
        logic = ArtifactoryDetector()

        output = logic.analyze_string(payload, 1, 'mock_filename')
        assert len(output) == int(should_flag)
