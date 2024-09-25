from rdf_graph_migration import download_latest_envthes_release_from_github, substitute_uri_domain

if __name__ == '__main__':
    # settings
    download_directory="./temp/"
    old_uri_prefix_lter_eu = "http://vocabs.lter-europe.net/"
    new_uri_prefix_elter_ri = "https://vocabs.ci.elter-ri.eu/"

    # download file from latest release from github
    ttl_file = download_latest_envthes_release_from_github(download_directory)

    # create new file with changed uris (and sameAs triples for tracking changes)
    substitute_uri_domain(ttlfile=ttl_file,
                          old_uri_prefix=old_uri_prefix_lter_eu,
                          new_uri_prefix=new_uri_prefix_elter_ri)
