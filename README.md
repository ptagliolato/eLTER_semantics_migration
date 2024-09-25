# eLTER semantic graphs migration
Functions to migrate LTER-Europe semantic graphs to eLTER-RI

Aim of the code is to support migration of LTER Europe vocabularies to the forecoming eLTER-RI.

Semantic resources will be maintained by the new Research Infrastructure and the decision was taken to 
expose the entities with URIs pertaining to eLTER-RI domain.
The main script in this repository 
* collects the most recent release of the vocabularies maintained within the LTER-Europe GitHub repository, 
* substitutes the old domain-name with the new one
* adds equivalence relations linking the old and the new URIs

## example usage

    download_directory="./temp/"
    old_uri_prefix_lter_eu = "http://vocabs.lter-europe.net/"
    new_uri_prefix_elter_ri = "https://vocabs.ci.elter-ri.eu/"
    ttl_file = download_latest_envthes_release_from_github(download_directory)
    substitute_uri_domain(ttlfile = ttl_file,
                          old_uri_prefix = old_uri_prefix_lter_eu,
                          new_uri_prefix = new_uri_prefix_elter_ri)

 
The code above creates a "temp" directory with a subfolder "LTER-Europe-EnvThes-<hash>" in the current folder, where
it puts the 
* EnvThes.ttl (EnvThes turtle file from the latest release of the repo LTER-Europe/EnvThes) 
* EnvThes_new_uris.ttl (a file with the substituted domain and added equivalence triples, 
e.g. <old_uri> owl:sameAs <new_uri>) 

## Acknowledgement
This work is funded by eLTER-Plus H2020 Project and ENRICH HEU Project