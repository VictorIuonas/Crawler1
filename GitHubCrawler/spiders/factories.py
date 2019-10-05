from GitHubCrawler.spiders.services import ConfigService, OutputUrlService
from GitHubCrawler.spiders.use_cases import SearchResultLinkExtractorUseCase, SearchUrlGeneratorUseCase, \
    RedirectLinkExtractorUseCase


def build_search_url_generator() -> SearchUrlGeneratorUseCase:
    return SearchUrlGeneratorUseCase(ConfigService())


def build_git_search_result_extractor_use_case() -> SearchResultLinkExtractorUseCase:
    return SearchResultLinkExtractorUseCase(OutputUrlService())


def build_redirect_link_extractor_use_case() -> RedirectLinkExtractorUseCase:
    return RedirectLinkExtractorUseCase(ConfigService())
