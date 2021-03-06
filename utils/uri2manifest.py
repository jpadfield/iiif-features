import argparse
import os
import uuid

def items2Manifest(source_file: str, output: str, version: str):
    with open(source_file, 'r') as reader, open(output, 'w') as writer:
        uid = uuid.uuid1()
        if version == '2':
            # P2 manifest
            manifest_start = """
            {
              "@context": "http://iiif.io/api/presentation/2/context.json",
              "@id": "https://%(uid)s",
              "@type": "sc:Manifest",
              "label": "[Click to edit label]",
              "metadata": [],
              "description": [
                {
                  "@value": "[Click to edit description]",
                  "@language": "en"
                }
              ],
              "license": "https://creativecommons.org/licenses/by/3.0/",
              "attribution": "[Click to edit attribution]",
              "sequences": [
                {
                  "@id": "https://%(uid)s",
                  "@type": "sc:Sequence",
                  "label": "Normal Sequence",
                  "canvases": [
            """ % locals()
        else:
            # P3 manifest
            manifest_start = """
            {
              "@context": [
                "http://www.w3.org/ns/anno.jsonld",
                "http://iiif.io/api/presentation/3/context.json"
              ],
              "id": "https://%(uid)s",
              "type": "Manifest",
              "label": {
                "en": [
                  "LayerStack demo"
                ]
              },
              "metadata": [
                {
                  "label": {
                    "en": [
                      "Comment"
                    ]
                  },
                  "value": {
                    "@none": [
                      "LayerStack demo"
                    ]
                  }
                }
              ],
              "summary": {
                "en": [
                  "LayerStack demo"
                ]
              },
              "thumbnail": [
                {
                  "id": "#TODO",
                  "type": "Image",
                  "width": 200,
                  "height": 300,
                  "service": {
                    "id": "#TODO",
                    "type": "ImageService2",
                    "profile": "level1"
                  }
                }
              ],
              "rights": "https://creativecommons.org/licenses/by/4.0/",
              "homepage": {
                "id": "https://vanda.github.io/iiif-features/img/compariscope_manifest.json",
                "type": "Text",
                "label": {
                  "en": [
                    "LayerStack demo"
                  ]
                },
                "format": "text/html"
              },
              "items": [
            """ % locals()
        writer.write(manifest_start)

        i = 0
        for imgDataStr in reader:
            i += 1
            imgData = imgDataStr.replace('\n', '').split(' ')
            imgURI = imgData[0]
            imgW = imgData[1]
            imgH = imgData[2]

            manifest_item = ',' if i > 1 else ''

            if version == '2':
                # P2 manifest
                manifest_item += """
                {
                  "@id": "%(imgURI)s/canvas/%(i)s",
                  "@type": "sc:Canvas",
                  "label": "canvas %(i)s",
                  "width": %(imgW)s,
                  "height": %(imgH)s,
                  "images": [
                    {
                      "@context": "http://iiif.io/api/presentation/2/context.json",
                      "@id": "%(imgURI)s/annotation/%(i)s",
                      "@type": "oa:Annotation",
                      "motivation": "sc:painting",
                      "resource": {
                        "@id": "%(imgURI)s/full/full/0/default",
                        "@type": "dctypes:Image",
                        "format": "image/png",
                        "service": {
                          "@context": "http://iiif.io/api/image/2/context.json",
                          "@id": "%(imgURI)s",
                          "profile": [
                            "http://iiif.io/api/image/2/level1.json",
                            {
                              "formats": [
                                "png",
                                "jpg"
                              ],
                              "qualities": [
                                "native",
                                "color",
                                "gray"
                              ],
                              "supports": [
                                "regionByPct",
                                "sizeByForcedWh",
                                "sizeByWh",
                                "sizeAboveFull",
                                "rotationBy90s",
                                "mirroring",
                                "gray"
                              ]
                            }
                          ]
                        },
                        "width": %(imgW)s,
                        "height": %(imgH)s
                      },
                      "on": "%(imgURI)s/canvas/%(i)s"
                    }
                  ],
                  "related": ""
                }""" % locals()
            else:
                # P3 manifest
                manifest_item += """
                {
                  "id": "%(imgURI)/canvas/%(i)s",
                  "type": "Canvas",
                  "label": {
                    "en": [
                      "canvas %(i)s"
                    ]
                  },
                  "summary": {
                    "en": [
                      ""
                    ]
                  },
                  "width": %(imgW)s,
                  "height": %(imgH)s,
                  "requiredStatement": {
                    "label": {
                      "en": [
                        ""
                      ]
                    },
                    "value": {
                      "en": [
                        ""
                      ]
                    }
                  },
                  "items": [
                    {
                      "id": "%(imgURI)s/list/%(i)s",
                      "type": "AnnotationPage",
                      "items": [
                        {
                          "id": "%(imgURI)s/annotation/%(i)s",
                          "type": "Annotation",
                          "motivation": "painting",
                          "body": {
                            "@id": "%(imgURI)s/full/full/0/default",
                            "type": "Image",
                            "format": "img/jpeg",
                            "width": %(imgW)s,
                            "height": %(imgH)s,
                            "service": {
                              "id": "%(imgURI)s",
                              "type": "ImageService2",
                              "profile": "level1"
                            }
                          },
                          "target": "%(imgURI)s/canvas/%(i)s"
                        }
                      ]
                    }
                  ]
                }""" % locals()

            writer.write(manifest_item)

        if version == '2':
            # P2 manifest
            manifest_end = """
                  ]
                }
              ]
            }
            """
        else:
            # P3 manifest
            manifest_end = """
              ],
              "structures": [
              ]
            }
            """
        writer.write(manifest_end)


if __name__ == "__main__":
    # Create our Argument parser and set its description
    parser = argparse.ArgumentParser(
        description="Script that generates IIIF manifest items from a file listing IIIF Image URIs",
    )

    # Add the arguments:
    #   - source_file: the source file we want to convert
    #   - output: the destination where the output should go
    #   - version: the version of the IIIF Presentation API to use

    # Note: the use of the argument type of argparse.FileType could
    # streamline some things
    parser.add_argument(
        'source_file',
        help='The location of the source '
    )

    parser.add_argument(
        '--version',
        help='IIIF Presentation API verion (default: 2)',
        default=2
    )

    parser.add_argument(
        '--output',
        help='Output file (default: source_file appended with `.json`',
        default=None
    )

    # Parse the args (argparse automatically grabs the values from
    # sys.argv)
    args = parser.parse_args()

    s_file = args.source_file
    d_file = args.output
    p_version = args.version

    # If the destination file wasn't passed, then assume we want to
    # create a new file based on the old one
    if d_file is None:
        file_path, file_extension = os.path.splitext(s_file)
        d_file = '%(file_path)s%(file_extension)s.json' % locals()

    items2Manifest(s_file, d_file, p_version)
