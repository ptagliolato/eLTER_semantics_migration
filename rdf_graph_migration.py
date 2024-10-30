__author__ = "Paolo Tagliolato (CNR-IREA) ptagliolato"
__version__ = "0.0.1"
import json
import urllib.request
import os
import tempfile
import rdflib
from io import BytesIO
from zipfile import ZipFile
from rdflib.namespace import OWL
from rdflib import Graph
from pathlib import Path


def download_single_file_from_github_latest_release(user_repo:str, filepath_within_zip_root:str,
                                                    downloadpath:str):
    """
    Download one file from the latest release published on a github repo.
    :param user_repo:
    :param filepath_within_zip_root:
    :param downloadpath:
    :return: path to the downloaded file or False if no new release is present.
    """
    # TODO: implement check of already downloaded release files
    if(not downloadpath.endswith("/")):
        downloadpath=f"{downloadpath}/"
    url=f"https://api.github.com/repos/{user_repo}/releases/latest"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    releaseVersion = data["tag_name"]
    releaseZipUrl = data["zipball_url"]

    # TODO: read last downloaded version from somewhere. Here "False" makes the next if always true
    lastDownloadedVersion = False
    # TODO: check if latest on github is > last downloaded version
    #  For this it is needed to check some process MD to be defined and saved somewhere.
    if (releaseVersion != lastDownloadedVersion):
        # with urllib.request.urlopen(releaseZipUrl):
        url_ttl = urllib.request.urlopen(releaseZipUrl)
        with ZipFile(BytesIO(url_ttl.read())) as my_zip_file:
            # TODO: save some file in the same root directory to keep track of release version.
            # print([fname for fname in my_zip_file.namelist()])
            rootfolder = [fname for fname in my_zip_file.namelist()][0]
            print(rootfolder)
            my_zip_file.extract(f"{rootfolder}{filepath_within_zip_root}", path=downloadpath)

        my_zip_file.close()
        return (f"{downloadpath}{rootfolder}{filepath_within_zip_root}")
    else:
        return (False)


def download_latest_envthes_release_from_github(downloadpath:str) -> str|bool:
    """
    Download the EnvThes.ttl file from the latest release published on github LTER-Europe/EnvThes repo.
    :param downloadpath:
    :return: path to the downloaded file or False if no new release is present.
    """
    return(download_single_file_from_github_latest_release("LTER-Europe/EnvThes", "EnvThes.ttl", downloadpath))


def get_triples_tracking_modified_uri(old, new, equivalence_predicate:rdflib.term.URIRef = OWL.sameAs):
    """
    create triples tracking changes from old to new uri.
    E.g.
    return the triple
    ((<old>, owl:sameAs, <new>))
    :param old:
    :param new:
    :param equivalence_predicate:
    :return:
    """
    res = list()
    res.append((old, equivalence_predicate, new))
    res.append((new, equivalence_predicate, old))
    return res


def substitute_uri_domain(ttlfile:str, old_uri_prefix:str, new_uri_prefix:str,
                          destination_folder=None
                          ) -> str:
    """
    make a copy of the ttlfile,
    change all occurrences of old_uri_prefix into new_uri_prefix
    and the triples returned by method get_triples_tracking_modified_uri
    e.g.
    <old_uri> owl:sameAs <new_uri>
    for each substituted <old_uri>

    :param ttlfile:
    :param old_uri_prefix:
    :param new_uri_prefix:
    :param destination_folder:

    :return:
    """


    # check input
    assert os.path.isfile(ttlfile), "input ttlfile must be a valid path to a file"
    if destination_folder:
        assert os.path.isdir(destination_folder), "destination_folder must be a path to an existing folder"
    #assert equivalence_predicate.__class__ == rdflib.term.URIRef

    file_dir= os.path.dirname(ttlfile)
    if not destination_folder:
        destination_folder = file_dir

    #output_file_1 = join(file_dir, f"{Path(ttlfile).stem}_new_uris.{Path(ttlfile).suffix}")
    fdesc, output_file_1 = tempfile.mkstemp(suffix=Path(ttlfile).suffix, prefix="new_uri_",
                                            dir=destination_folder, text=True)
    os.close(fdesc)

    ttlfile_new = os.path.join(file_dir, f"{Path(ttlfile).stem}_new_uris.{Path(ttlfile).suffix}")

    #Path(ttlfile).stem
    #Path(ttlfile).suffix
    #Path(ttlfile).name

    g = Graph()
    # get the data
    g.parse(ttlfile)

    qres=g.query('select distinct ?s where {'
            '?s ?p ?o.'
            f"FILTER regex(str(?s), \"{old_uri_prefix}\")"
            '}')

    # save the list of all (distinct) subjects
    old_uris=[row.s for row in qres]

    # read ttl file with old uris
    with open(ttlfile, 'r') as file:
        old_data = file.read()
    # replace old with new uris
    new_data = old_data.replace(old_uri_prefix, new_uri_prefix)

    # temp outfile
    f = open(output_file_1,'w')
    f.write(new_data)
    f.close()

    # rdflib manipulation changing all triples with one of the olduris?

    # read the new ttl file with rdflib, then add triples olduris sameAs newuris
    g_new = Graph()
    # get the data
    g_new.parse(output_file_1)
    for old_uri in old_uris:
        new_uri_string = str(old_uri).replace(old_uri_prefix,new_uri_prefix)
        new_uri = rdflib.URIRef(new_uri_string)
        # add the following triples
        triples = get_triples_tracking_modified_uri(old_uri, new_uri)
        for t in triples:
            g_new.add(t)
        #g_new.add((old_uri, equivalence_predicate, new_uri))

    os.path.join(file_dir, f"{Path(ttlfile).stem}_new.{Path(ttlfile).suffix}")
    g_new.serialize(destination=ttlfile_new)

    os.remove(output_file_1)
    return


