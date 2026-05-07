# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "standard_app" / "templates" / "sap_form.html"
t = p.read_text(encoding="utf-8")

if 'navigateToStation(4)' not in t:
    t = t.replace(
        """                <button class=\"btn btn-sm btn-outline-primary\" onclick=\"navigateToStation(3)\">
                    <i class=\"fas fa-desktop me-1\"></i>Station 3 <i id=\"nav_tick_s3\" class=\"fas fa-check-circle ms-1 text-outline-primary hidden\"></i>
                </button>
            </div>""",
        """                <button class=\"btn btn-sm btn-outline-primary\" onclick=\"navigateToStation(3)\">
                    <i class=\"fas fa-desktop me-1\"></i>Station 3 <i id=\"nav_tick_s3\" class=\"fas fa-check-circle ms-1 text-outline-primary hidden\"></i>
                </button>
                <button class=\"btn btn-sm btn-outline-primary\" onclick=\"navigateToStation(4)\">
                    <i class=\"fas fa-desktop me-1\"></i>Station 4 <i id=\"nav_tick_s4\" class=\"fas fa-check-circle ms-1 text-outline-primary hidden\"></i>
                </button>
            </div>""",
        1,
    )

if 'actionBarS4Wrapper' not in t:
    t = t.replace(
        """                    <button class=\"btn btn-custom btn-danger-custom\" onclick=\"cancel_station3()\">Cancel</button>
                </div>
            </div>
            <!-- <div style=\"width: 1px; height: 24px; background: #cbd5e1; margin: 0 0.5rem;\"></div> -->""",
        """                    <button class=\"btn btn-custom btn-danger-custom\" onclick=\"cancel_station3()\">Cancel</button>
                </div>
            </div>
            <div class=\"d-flex align-items-center gap-2 hidden\" id=\"actionBarS4Wrapper\">
                <div class=\"action-bar\" id=\"actionBarS4\">
                    <button id=\"save_btn_s4\" class=\"btn btn-custom btn-success-custom\"><i
                            id=\"save_icon_s4\" class=\"fas fa-save\"></i>
                        <span id=\"save_text_s4\">Save</span></button>
                    <button id=\"next_btn_s4\" class=\"btn btn-custom btn-brand\" onclick=\"continue_station4()\">Next <i
                            class=\"fas fa-arrow-right\"></i></button>
                    <button class=\"btn btn-custom btn-secondary-custom\" onclick=\"clear_station4()\">Clear</button>
                    <button class=\"btn btn-custom btn-danger-custom\" onclick=\"cancel_station4()\">Cancel</button>
                </div>
            </div>
            <!-- <div style=\"width: 1px; height: 24px; background: #cbd5e1; margin: 0 0.5rem;\"></div> -->""",
        1,
    )

t = t.replace(
    "document.getElementById('station3_container').classList.add('hidden');",
    "document.getElementById('station3_container').classList.add('hidden');\n            document.getElementById('station4_container').classList.add('hidden');",
    1,
)
t = t.replace(
    "document.getElementById('actionBarS3Wrapper').classList.add('hidden');",
    "document.getElementById('actionBarS3Wrapper').classList.add('hidden');\n            document.getElementById('actionBarS4Wrapper').classList.add('hidden');",
    1,
)

if 'stationFromUrl === "4"' not in t:
    t = t.replace(
        """            } else if (stationFromUrl === "3") {
                document.getElementById('station3_container').classList.remove('hidden');
                document.getElementById('headerStationBadge').textContent = 'Station 3';
                document.getElementById('actionBarS3Wrapper').classList.remove('hidden');
                highlightActiveStation(3);
} else {""",
        """            } else if (stationFromUrl === "3") {
                document.getElementById('station3_container').classList.remove('hidden');
                document.getElementById('headerStationBadge').textContent = 'Station 3';
                document.getElementById('actionBarS3Wrapper').classList.remove('hidden');
                highlightActiveStation(3);
            } else if (stationFromUrl === "4") {
                document.getElementById('station4_container').classList.remove('hidden');
                document.getElementById('headerStationBadge').textContent = 'Station 4';
                document.getElementById('actionBarS4Wrapper').classList.remove('hidden');
                highlightActiveStation(4);
} else {""",
        1,
    )

marker = """                    </div>
                </div>
            </div>
        </div>


    </div>

    <script src=\"{% static 'vendor/bootstrap/bootstrap.bundle.min.js' %}\"></script>"""

snippet = """        <div id=\"station4_container\" class=\"station-container hidden\">
            <div class=\"row h-100 g-2\">
                <div class=\"col-12\">
                    <div class=\"row g-2\" style=\"height: 60vh;\">
                        <div class=\"col-lg-3 h-120\">
                            <div class=\"form-card h-100\">
                                <div class=\"card-header py-1\"><span>Testing Parameters</span></div>
                                <div class=\"card-body py-2\">
                                    <div class=\"row g-1\">
                                        <div class=\"col-12 sap-auto-field\"><label for=\"standard_s4\" class=\"form-label\">Standard</label><select id=\"standard_s4\" name=\"standard_s4\" class=\"form-select\"><option value=\"\">Select</option>{% for s in valve_standards %}<option value=\"{{ s }}\">{{ s }}</option>{% endfor %}</select></div>
                                        <div class=\"col-12\"><label class=\"form-label\">Size</label><div class=\"sap-manual-label\"><span class=\"sap-manual-value\" id=\"size_label_s4\">Select Size</span></div></div>
                                        <div class=\"col-12 sap-auto-field\"><label for=\"size_s4\" class=\"form-label\">Size</label><select id=\"size_s4\" name=\"size_s4\" class=\"form-select\"><option value=\"\">Select</option>{% for s in valve_sizes %}<option value=\"{{ s }}\">{{ s }}</option>{% endfor %}</select></div>
                                        <div class=\"col-12\"><label class=\"form-label\">Class</label><div class=\"sap-manual-label\"><span class=\"sap-manual-value\" id=\"class_label_s4\">Select Class</span></div></div>
                                        <div class=\"col-12 sap-auto-field\"><label for=\"class_s4\" class=\"form-label\">Class</label><select id=\"class_s4\" name=\"class_s4\" class=\"form-select\"><option value=\"\">Select</option>{% for c in valve_classes %}<option value=\"{{c}}\">{{c}}</option>{% endfor %}</select></div>
                                        <div class=\"col-12\"><label class=\"form-label\">Body Material</label><div class=\"sap-manual-label\"><span class=\"sap-manual-value\" id=\"body_material_label_s4\">Select Body Material</span></div></div>
                                        <div class=\"col-12 sap-auto-field\"><label for=\"body_material_s4\" class=\"form-label\">Body Material</label><select id=\"body_material_s4\" name=\"body_material_s4\" class=\"form-select\"><option value=\"\">Select</option>{% for m in shell_materials %}<option value=\"{{m}}\">{{m}}</option>{% endfor %}</select></div>
                                        <div class=\"col-12\"><label for=\"duration_type_s4\" class=\"form-label\">Duration Type</label><select id=\"duration_type_s4\" name=\"duration_type_s4\" class=\"form-select sap-custom-select\"><option value=\"\">Select</option>{% for d in duration_types %}<option value=\"{{d}}\">{{d}}</option>{% endfor %}</select></div>
                                        <div class=\"col-12\"><label class=\"form-label\">Type</label><div class=\"sap-manual-label\"><span class=\"sap-manual-value\" id=\"type_label_s4\">Select Type</span></div></div>
                                        <div class=\"col-12 sap-auto-field\"><label for=\"type_s4\" class=\"form-label\">Type</label><select id=\"type_s4\" name=\"type_s4\" class=\"form-select\"><option value=\"\">Select</option>{% for t in valve_types %}<option value=\"{{t}}\">{{t}}</option>{% endfor %}</select></div>
                                        <div class=\"col-12\"><label for=\"pressureunit_s4\" class=\"form-label\">Pressure Unit</label><select id=\"pressureunit_s4\" name=\"pressureunit_s4\" class=\"form-select sap-custom-select\"><option value=\"\" selected disabled hidden>Select</option><option value=\"PSI\">PSI</option><option value=\"BAR\">BAR</option></select></div>
                                        <div class=\"col-12 text-end mt-3 d-none\"><button id=\"load_btn_s4\" class=\"btn btn-sm btn-brand px-3\" onclick=\"load_station4()\">Load</button></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class=\"col-lg-9 d-flex flex-column gap-2 h-100\">
                            <div class=\"form-card\" style=\"flex: 0 0 35%;\">
                                <div class=\"card-header py-1\">Valve Details</div>
                                <div class=\"card-body py-2\">
                                    {% include \"standard_app/_valve_details_fields.html\" with station_suffix=\"s4\" serial_id=\"VALVE_SER_NO_s4\" assembly_id=\"ASSEMBLY_NO_s4\" serial_name=\"VALVE_SER_NO_s4\" assembly_name=\"ASSEMBLY_NO_s4\" %}
                                </div>
                            </div>
                            <div class=\"form-card\" style=\"flex: 1;\">
                                <div class=\"card-header py-1\">Item / Part Details</div>
                                {% include \"standard_app/_item_details_fields.html\" with station_suffix=\"s4\" %}
                            </div>
                        </div>
                    </div>
                </div>
                <div class=\"col-12\" style=\"height: calc(30vh - 1rem);\">
                    <div class=\"form-card pressuretable4 h-100\">
                        <div class=\"d-flex h-100\">
                            <div class=\"flex-grow-1 h-100 overflow-auto border-end\">
                                <div class=\"card-header py-1 sticky-top\">Pressure Tests</div>
                                <table class=\"table mb-0 custom-table table-sm\">
                                    <thead><tr><th>Test Type</th><th id=\"pressure_header_s4\">Pressure</th><th>Duration (Sec)</th><th>Action</th></tr></thead>
                                    <tbody id=\"pressureTableBody4\"><tr class=\"empty-state\"><td colspan=\"4\" class=\"text-center py-4\" style=\"color: #94a3b8; font-style: italic;\"><i class=\"fas fa-info-circle me-1\"></i>Select testing parameters and click \"Load\" to view pressure and duration.</td></tr></tbody>
                                </table>
                            </div>
                            <div class=\"degreetable4 hidden\" style=\"width: 20%;\"><div class=\"card-header py-1 sticky-top\">Degrees</div><table class=\"table mb-0 custom-table table-sm\"><thead><tr><th>Open</th><th>Close</th></tr></thead><tbody></tbody></table></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>


"""

if 'id="station4_container"' not in t:
    if marker not in t:
        raise SystemExit("marker not found in sap_form.html")
    t = t.replace(marker, snippet + marker, 1)

# Copy station-4 JS from form.html (from load_station4 through save listener for s4)
form = (ROOT / "standard_app" / "templates" / "form.html").read_text(encoding="utf-8")
start = form.find("        function load_station4()")
end = form.find("        function cancel_station3()", start)
if start == -1 or end == -1:
    raise SystemExit("could not find load_station4 block in form.html")
block = form[start:end]

if "function load_station4()" not in t:
    ins = t.find("        function cancel_station3()")
    if ins == -1:
        raise SystemExit("cancel_station3 not in sap_form")
    t = t[:ins] + block + t[ins:]

# mandatory + validator s4
if "mandatory_fields_s4" not in t:
    t = t.replace(
        '        const mandatoryS3 = [{% for f in mandatory_fields_s3 %}"{{ f|escapejs }}"{% if not forloop.last %}, {% endif %} {% endfor %}];',
        '        const mandatoryS3 = [{% for f in mandatory_fields_s3 %}"{{ f|escapejs }}"{% if not forloop.last %}, {% endif %} {% endfor %}];\n        const mandatoryS4 = [{% for f in mandatory_fields_s4 %}"{{ f|escapejs }}"{% if not forloop.last %}, {% endif %} {% endfor %}];',
        1,
    )
    t = t.replace(
        "        let valveValidatorS3 = null;",
        "        let valveValidatorS3 = null;\n        let valveValidatorS4 = null;",
        1,
    )
    t = t.replace(
        """        if (document.getElementById('station3_container') && mandatoryS3.length > 0) {
            valveValidatorS3 = new FormValidator('station3_container', valveValidatorConfig(mandatoryS3));
        }""",
        """        if (document.getElementById('station3_container') && mandatoryS3.length > 0) {
            valveValidatorS3 = new FormValidator('station3_container', valveValidatorConfig(mandatoryS3));
        }
        if (document.getElementById('station4_container') && mandatoryS4.length > 0) {
            valveValidatorS4 = new FormValidator('station4_container', valveValidatorConfig(mandatoryS4));
        }""",
        1,
    )

p.write_text(t, encoding="utf-8")
print("sap_form.html updated")
