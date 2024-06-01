{{/* api */}}

{{- define "orch.checksum/config" -}}
{{- $config := .Files.Get "files/services/api/config.yml" | sha256sum -}}
{{- $tools := .Files.Get "files/services/api/tools.yml" | sha256sum -}}
{{- $fluent_config := .Files.Get "files/services/api/fluent-config.yml" | sha256sum -}}
{{- $fluent_parsers := .Files.Get "files/services/api/fluent-parsers.yml" | sha256sum -}}
{{- $scm_repos := .Files.Get "files/services/api/scm_repos.yml" | sha256sum -}}
{{ print $config $tools $scm_repos $fluent_config $fluent_parsers | sha256sum }}
{{- end -}}
