{{/* prometheus */}}

{{- define "orch.checksum/config" -}}
{{- $config := .Files.Get "templates/prometheus/configmap.yml" | sha256sum -}}
{{ print $config | sha256sum }}
{{- end -}}
