from django import forms


FILTER_FIELDSET_CONFIG = [
    {
        "legend": "PDU Protocol",
        "slug": "protocol",
        "fields": [
            {"name": "pdu_type", "label": "PDU Type", "kind": "text"},
        ],
    },
    {
        "legend": "Temporal",
        "slug": "temporal",
        "fields": [
            {"name": "start_time", "label": "Start Time", "kind": "datetime"},
            {"name": "end_time", "label": "End Time", "kind": "datetime"},
        ],
    },
    {
        "legend": "Tactical",
        "slug": "tactical",
        "fields": [
            {"name": "force_id", "label": "Force ID", "kind": "number"},
            {"name": "site_id", "label": "Site ID", "kind": "number"},
            {"name": "application_id", "label": "Application ID", "kind": "number"},
            {"name": "exercise_id", "label": "Exercise ID", "kind": "number"},
        ],
    },
    {
        "legend": "Entity",
        "slug": "entity",
        "fields": [
            {"name": "entity_id", "label": "Entity ID", "kind": "number"},
            {"name": "entity_kind", "label": "Entity Kind", "kind": "text"},
            {"name": "entity_domain", "label": "Entity Domain", "kind": "text"},
            {"name": "entity_category", "label": "Entity Category", "kind": "text"},
        ],
    },
    {
        "legend": "Raw SQL",
        "slug": "raw_sql",
        "fields": [
            {"name": "raw_sql", "label": "Raw SQL", "kind": "text"},
            {"name": "show_malformed", "label": "Show Malformed", "kind": "boolean"},
        ],
    },
]


class PlaybackSenderForm(forms.Form):
    duration_seconds = forms.IntegerField(
        label='Duration (seconds)',
        min_value=1,
        initial=30,
        help_text='How long to send synthetic PDUs.',
    )
    destination_host = forms.GenericIPAddressField(
        label='Destination IP',
        initial='127.0.0.1',
        protocol='both',
        unpack_ipv4=False,
        help_text='Target address for the synthetic DIS traffic.',
    )
    destination_port = forms.IntegerField(
        label='Destination port',
        min_value=1,
        max_value=65535,
        initial=3500,
        help_text='Target UDP port for the synthetic DIS traffic.',
    )


class ConnectionSettingsForm(forms.Form):
    listen_host = forms.GenericIPAddressField(
        label='Listen Host',
        initial='0.0.0.0',
        protocol='both',
        unpack_ipv4=False,
        help_text='Local address to bind for DIS ingestion.',
    )
    listen_port = forms.IntegerField(
        label='Listen Port',
        min_value=1,
        max_value=65535,
        initial=3500,
        help_text='UDP port to receive DIS packets on.',
    )


class PduFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': ''}) # Keep blank for Pico default styling

    def get_filter_fieldsets(self):
        return FILTER_FIELDSET_CONFIG

    filter_builder_state = forms.CharField(widget=forms.HiddenInput(), required=False)

    # @PDU Type Filter, SPEC_FILTER_PROTOCOL, code_impl, SPEC_FILTER_PROTOCOL
    pdu_type = forms.MultipleChoiceField(
        label='PDU Type',
        required=False,
    )

    # @Time Range Filter, SPEC_FILTER_TEMPORAL, code_impl, SPEC_FILTER_TEMPORAL
    start_time = forms.DateTimeField(required=False)
    end_time = forms.DateTimeField(required=False)

    # @Tactical Filter, SPEC_FILTER_TACTICAL, code_impl, SPEC_FILTER_TACTICAL
    force_id = forms.ChoiceField(required=False)
    site_id = forms.IntegerField(required=False)
    application_id = forms.IntegerField(required=False)
    exercise_id = forms.IntegerField(required=False)

    # @Entity Filter, SPEC_FILTER_ENTITY, code_impl, SPEC_FILTER_ENTITY
    entity_id = forms.IntegerField(required=False)
    entity_kind = forms.ChoiceField(required=False)
    entity_domain = forms.ChoiceField(required=False)
    entity_category = forms.ChoiceField(required=False)

    # @Diagnostic Filter, SPEC_FILTER_DIAGNOSTIC, code_impl, SPEC_FILTER_DIAGNOSTIC
    raw_sql = forms.CharField(required=False)
    show_malformed = forms.BooleanField(required=False)
