{{/* egressgateway */}}

{{- define "istio.control_panel" -}}
{{- if (eq .Values.job_namespace .Release.Namespace) -}}
{{ .Values.scan_control_panel | default .Values.control_panel }}
{{- else if (eq .Values.namespace .Release.Namespace) -}}
{{ .Values.engine_control_panel | default .Values.control_panel }}
{{- else -}}
UNKNOWN
{{- end -}}
{{- end -}}