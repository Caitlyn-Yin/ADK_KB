name: 'Release Action'
description: 'Creates a GitHub release'
inputs:
  files:
    description: 'Glob pattern of files to upload as release assets'
    required: true
  tag_name:
    description: 'The name of the tag for the release'
    required: true
  name:
    description: 'The name of the release'
    required: true
  body:
    description: 'The body text of the release'
    required: true
  draft:
    description: 'Whether to create a draft release (true/false)'
    required: false
    default: 'false'
  prerelease:
    description: 'Whether this is a pre-release (true/false)'
    required: false
    default: 'false'
  github_token:
    description: 'GitHub token with repo scope'
    required: true

runs:
  using: 'composite'
  steps:
    - name: Install PyGithub
      shell: bash
      run: pip install pygithub
    - name: Create Release
      id: create_release
      shell: bash
      run: |
        python3 $GITHUB_ACTION_PATH/release.py
      env:
        GITHUB_TOKEN: ${{ inputs.github_token }}
        FILES: ${{ inputs.files }}
        TAG_NAME: ${{ inputs.tag_name }}
        NAME: ${{ inputs.name }}
        BODY: ${{ inputs.body }}
        DRAFT: ${{ inputs.draft }}
        PRERELEASE: ${{ inputs.prerelease }}
        GITHUB_REPOSITORY: ${{ github.repository }}
