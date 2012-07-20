from evelink.parsing.industry_jobs import parse_industry_jobs

class Corp(object):
    """Wrapper around /corp/ of the EVE API.

    Note that a valid corp API key is required.
    """

    def __init__(self, api):
        self.api = api

    def industry_jobs(self):
        """Get a list of jobs for a corporation."""

        api_result = self.api.get('corp/IndustryJobs')

        return parse_industry_jobs(api_result)
