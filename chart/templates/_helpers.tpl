{{- define "orch.image" -}}
{{- $tag := index .Values "tag" .Serv -}}
{{- $name := index .Values .Serv "name" -}}

{{- if not $name -}}
{{- $name = print "orch-" .Serv }}
{{- end -}}

{{ regexMatch "^sha256:.*" $tag | ternary .Values.prodRegistry .Values.devRegistry }}/{{ $name }}{{ regexMatch "^sha256:.*" $tag | ternary "@" ":" }}{{ $tag }}
{{- end -}}


{{- define "orch.resources" -}}
{{- if (index .Values .Serv "resources") -}}
{{- $ratio := .Values.resource_ratio }}
{{- $cpu := mulf (index .Values .Serv "resources" "cpu") $ratio -}}
{{- $memory := mulf (index .Values .Serv "resources" "memory") $ratio -}}
resources:
  limits:
    cpu: {{ $cpu }}m
    memory: {{ $memory }}Mi
  requests:
    cpu: {{ $cpu }}m
    memory: {{ $memory }}Mi
{{- end -}}
{{- end -}}
