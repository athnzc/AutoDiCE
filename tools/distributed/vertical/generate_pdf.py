from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

OUTPUT = "AutoDiCE_Pipeline.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'Title', parent=styles['Title'],
    fontSize=24, leading=30, textColor=colors.HexColor('#1a237e'),
    spaceAfter=6
)
subtitle_style = ParagraphStyle(
    'Subtitle', parent=styles['Normal'],
    fontSize=12, textColor=colors.HexColor('#455a64'),
    spaceAfter=20, alignment=TA_CENTER
)
h1_style = ParagraphStyle(
    'H1', parent=styles['Heading1'],
    fontSize=16, leading=20, textColor=colors.HexColor('#1a237e'),
    spaceBefore=18, spaceAfter=8,
    borderPad=4
)
h2_style = ParagraphStyle(
    'H2', parent=styles['Heading2'],
    fontSize=13, leading=16, textColor=colors.HexColor('#0d47a1'),
    spaceBefore=12, spaceAfter=6
)
body_style = ParagraphStyle(
    'Body', parent=styles['Normal'],
    fontSize=10, leading=15, spaceAfter=8, alignment=TA_JUSTIFY
)
code_style = ParagraphStyle(
    'Code', parent=styles['Code'],
    fontSize=8.5, leading=13, backColor=colors.HexColor('#f5f5f5'),
    borderColor=colors.HexColor('#e0e0e0'), borderWidth=1,
    borderPad=6, spaceAfter=10, fontName='Courier'
)
bullet_style = ParagraphStyle(
    'Bullet', parent=styles['Normal'],
    fontSize=10, leading=15, leftIndent=16,
    bulletIndent=6, spaceAfter=4
)
note_style = ParagraphStyle(
    'Note', parent=styles['Normal'],
    fontSize=9, leading=13, textColor=colors.HexColor('#555555'),
    leftIndent=12, spaceAfter=6, fontStyle='italic'
)

def h1(text): return Paragraph(text, h1_style)
def h2(text): return Paragraph(text, h2_style)
def body(text): return Paragraph(text, body_style)
def code(text):
    escaped = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return Paragraph(escaped, code_style)
def bullet(text): return Paragraph(f"• &nbsp; {text}", bullet_style)
def note(text): return Paragraph(f"<i>Note: {text}</i>", note_style)
def space(n=0.3): return Spacer(1, n*cm)
def hr(): return HRFlowable(width="100%", thickness=1, color=colors.HexColor('#c5cae9'), spaceAfter=8)

def step_table(number, title, description):
    data = [[
        Paragraph(f"<b>Step {number}</b>", ParagraphStyle('sn', fontName='Helvetica-Bold',
            fontSize=11, textColor=colors.white, alignment=TA_CENTER)),
        Paragraph(f"<b>{title}</b><br/><font size=9>{description}</font>",
            ParagraphStyle('sd', fontName='Helvetica', fontSize=10, leading=14,
                textColor=colors.HexColor('#1a237e')))
    ]]
    t = Table(data, colWidths=[2.2*cm, 13.8*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#1a237e')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#e8eaf6')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [colors.HexColor('#e8eaf6')]),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#9fa8da')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (0,0), 4),
        ('LEFTPADDING', (1,0), (1,0), 10),
    ]))
    return t

story = []

# ── Cover ──────────────────────────────────────────────────────────────────
story.append(space(3))
story.append(Paragraph("AutoDiCE", title_style))
story.append(Paragraph("Model Splitting &amp; Distributed Execution Pipeline", subtitle_style))
story.append(hr())
story.append(space(0.5))
story.append(body(
    "This document describes every step involved in partitioning a deep neural network "
    "model and executing the resulting sub-models across multiple heterogeneous devices "
    "using the AutoDiCE framework. AutoDiCE combines ONNX-based model splitting, the "
    "ncnn inference engine, and MPI-based inter-device communication."
))
story.append(space(1))

# ── Overview table ──────────────────────────────────────────────────────────
overview_data = [
    [Paragraph("<b>Phase</b>", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
     Paragraph("<b>Tool / File</b>", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
     Paragraph("<b>Output</b>", ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white))],
    ["1. Configuration",      "interface.py  +  mapping.json",    "Layer-to-device assignment"],
    ["2. Model Splitting",    "onnx_split.py  (onnx_extract)",    "Per-device .onnx sub-models"],
    ["3. Format Conversion",  "onnx2ncnn",                        ".param + .bin files"],
    ["4. Code Generation",    "EngineCode  (interface.py)",       "multinode.cpp"],
    ["5. Compilation",        "cmake / make",                     "multinode binary"],
    ["6. Distributed Run",    "mpirun + rankfile",                "Inference result"],
]
ov_table = Table(overview_data, colWidths=[4.5*cm, 5.5*cm, 6*cm])
ov_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a237e')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f5f5'), colors.white]),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#9fa8da')),
    ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#c5cae9')),
    ('FONTSIZE', (0,1), (-1,-1), 9),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(ov_table)
story.append(PageBreak())

# ── Step 1 ──────────────────────────────────────────────────────────────────
story.append(h1("Phase 1 — Configuration"))
story.append(step_table(1, "Define devices and layer mapping",
    "Tell AutoDiCE how many devices you have and which model layers each device will run."))
story.append(space(0.4))

story.append(h2("1.1  Resource Dictionary  (interface.py)"))
story.append(body(
    "The <b>resourceid</b> dictionary in the <code>__main__</code> block of "
    "<b>interface.py</b> defines the available computing nodes. "
    "Each entry maps an integer ID to a node name following the convention "
    "<code>&lt;hostname&gt;_&lt;type&gt;&lt;core-ids&gt;</code>."
))
story.append(code(
    "# Two CPU nodes on the same laptop\n"
    "resourceid = { 1:'lenovo_cpu0', 2:'lenovo_cpu1' }\n\n"
    "# Laptop + Jetson\n"
    "resourceid = { 1:'lenovo_cpu0', 2:'jetson_cpu0' }\n\n"
    "# Three nodes\n"
    "resourceid = { 1:'laptop_cpu0', 2:'jetson_cpu0', 3:'jetson_cpu1' }"
))
story.append(body(
    "The number of entries in <b>resourceid</b> directly determines how many "
    "sub-models will be generated — one per entry."
))

story.append(h2("1.2  Platform List"))
story.append(body(
    "The <b>platforms</b> list contains the unique hostnames. "
    "This is used to generate the MPI <b>hostfile</b>."
))
story.append(code(
    "platforms = ['lenovo']            # single machine\n"
    "platforms = ['lenovo', 'jetson']  # two machines"
))

story.append(h2("1.3  mapping.json — Layer Assignment"))
story.append(body(
    "The <b>mapping.json</b> file is the partition plan. It is a JSON dictionary "
    "that maps each device name to the list of ONNX node names it will execute."
))
story.append(code(
    '{\n'
    '  "lenovo_cpu0": ["conv1_1", "norm1_1", "pool1_1", ...],  // 18 layers\n'
    '  "lenovo_cpu1": ["fc6_2", "relu6_2", "drop6_2", ...]     //  6 layers\n'
    '}'
))
story.append(body(
    "You can create this file manually or auto-generate it using the helper "
    "functions already present in interface.py:"
))
story.append(code(
    "gene = np.array([18]).astype(int)   # split after layer 18\n"
    "chromosome = ChromosomePartGen(gene, model_len, resourceid)\n"
    "random_map = MappingGenerator(resourceid, chromosome, input_model)\n"
    "save_json(random_map, './mapping.json')"
))
story.append(note(
    "The ConsistencyCheck() method in Interface verifies that every layer "
    "in the ONNX model appears exactly once in mapping.json before proceeding."
))
story.append(PageBreak())

# ── Step 2 ──────────────────────────────────────────────────────────────────
story.append(h1("Phase 2 — Model Splitting"))
story.append(step_table(2, "Extract sub-models from the original ONNX graph",
    "interface.py calls onnx_extract() once per device to produce a self-contained .onnx file."))
story.append(space(0.4))

story.append(h2("2.1  Input Preparation"))
story.append(body(
    "The original ONNX model is first passed through "
    "<b>format_onnx()</b> (in <code>onnx_map.py</code>), which runs ONNX shape "
    "inference and ensures every node has an explicit name. "
    "This is required so that layer names in mapping.json can be matched to graph nodes."
))
story.append(code(
    "origin_model = 'models/bvlcalexnet-9.onnx'\n"
    "input_model  = format_onnx(origin_model)   # produces format_bvlcalexnet-9.onnx"
))

story.append(h2("2.2  ModelSplit()"))
story.append(body(
    "The <b>ModelSplit()</b> method in the <b>Interface</b> class iterates over "
    "every node in resourceid and calls <b>onnx_extract()</b> for each one."
))
story.append(code(
    "for i in range(len(self.nodes)):\n"
    "    onnx_extract(self.model,\n"
    "                 './models/' + self.nodes[i] + '.onnx',\n"
    "                 self.mappings[self.nodes[i]])"
))
story.append(body(
    "<b>onnx_extract()</b> (in <code>onnx_split.py</code>) uses the ONNX "
    "<code>utils.extract_model()</code> utility to slice out the sub-graph "
    "corresponding to the assigned layers, automatically determining the "
    "correct input and output tensor names for each partition."
))

story.append(h2("2.3  Outputs"))
story.append(body("For each device, three files are produced in the <code>models/</code> directory:"))
for item in [
    "<b>lenovo_cpu0.onnx</b> — sub-graph for device 0",
    "<b>lenovo_cpu1.onnx</b> — sub-graph for device 1",
    "<b>sender.json</b> — which tensors each device sends to which rank",
    "<b>receiver.json</b> — which tensors each device receives from which rank",
    "<b>rankfile</b> — MPI rank-to-host mapping",
    "<b>hostfile</b> — list of hostnames for mpirun",
]:
    story.append(bullet(item))
story.append(space(0.3))
story.append(note(
    "The intermediate tensor between the two sub-models (e.g. fc6_2 for AlexNet, "
    "shape 4096 floats) becomes the output of sub-model 0 and the input of sub-model 1. "
    "GenerateComm() in interface.py identifies these boundary tensors automatically."
))
story.append(PageBreak())

# ── Step 3 ──────────────────────────────────────────────────────────────────
story.append(h1("Phase 3 — Format Conversion"))
story.append(step_table(3, "Convert .onnx sub-models to ncnn format",
    "onnx2ncnn converts each sub-model into .param (architecture) and .bin (weights) files."))
story.append(space(0.4))

story.append(body(
    "The <b>ncnn</b> inference engine used at runtime does not consume ONNX files directly. "
    "Each sub-model must be converted to ncnn's native format using the <b>onnx2ncnn</b> tool, "
    "which is built from source as part of the AutoDiCE cmake build."
))
story.append(code(
    "# run.sh does this automatically:\n"
    "for i in `ls ./models/*.onnx`; do\n"
    "    ./onnx2ncnn $i\n"
    "done"
))
story.append(h2("Output files"))
data = [
    [Paragraph("<b>File</b>", ParagraphStyle('th2', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
     Paragraph("<b>Contents</b>", ParagraphStyle('th2', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white))],
    ["lenovo_cpu0.param", "Text file describing all layers, connections, and parameters of sub-model 0"],
    ["lenovo_cpu0.bin",   "Binary file containing the float32 weights for sub-model 0"],
    ["lenovo_cpu1.param", "Text file describing all layers of sub-model 1"],
    ["lenovo_cpu1.bin",   "Binary weights for sub-model 1"],
]
t2 = Table(data, colWidths=[4.5*cm, 11.5*cm])
t2.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a237e')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f5f5'), colors.white]),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#9fa8da')),
    ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#c5cae9')),
    ('FONTSIZE', (0,1), (-1,-1), 9),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t2)
story.append(PageBreak())

# ── Step 4 ──────────────────────────────────────────────────────────────────
story.append(h1("Phase 4 — Code Generation"))
story.append(step_table(4, "Generate the distributed runtime (multinode.cpp)",
    "EngineCode in interface.py auto-generates C++ MPI code that loads and runs each sub-model."))
story.append(space(0.4))

story.append(body(
    "The <b>EngineCode</b> class in <code>interface.py</code> generates a complete "
    "C++ source file (<b>multinode.cpp</b>) that orchestrates the distributed inference. "
    "It produces one engine function per sub-model and a main() that initialises MPI."
))

story.append(h2("4.1  Per-device engine function"))
story.append(body(
    "For each device i, a function <code>model{i}_engine()</code> is generated that:"
))
for item in [
    "Loads the sub-model using <code>ncnn::Net::load_param()</code> and <code>load_model()</code>",
    "Calls <code>MPI_Irecv()</code> for every input tensor that comes from another device",
    "Runs inference with <code>ncnn::Extractor::input()</code> and <code>extract()</code>",
    "Calls <code>MPI_Isend()</code> for every output tensor that must go to another device",
    "Calls <code>MPI_Wait()</code> to ensure all transfers complete",
]:
    story.append(bullet(item))

story.append(space(0.3))
story.append(code(
    "// Generated example for rank 0 (lenovo_cpu0)\n"
    "void model0_engine(const char* imagepath, ncnn::Mat& data_0, ncnn::Mat& fc6_2) {\n"
    "    MPI_Request requests[1];\n"
    "    MPI_Status  status[1];\n"
    "    read_input(imagepath, data_0);\n"
    "    ncnn::Net lenovo_cpu0_model_0;\n"
    "    lenovo_cpu0_model_0.load_param(\"lenovo_cpu0.param\");\n"
    "    lenovo_cpu0_model_0.load_model(\"lenovo_cpu0.bin\");\n"
    "    ncnn::Extractor ex0 = lenovo_cpu0_model_0.create_extractor();\n"
    "    ex0.input(\"data_0\", data_0);\n"
    "    ex0.extract(\"fc6_2\", fc6_2);            // run layers 0-17\n"
    "    MPI_Isend((float*)fc6_2, fc6_2.total(),\n"
    "              MPI_FLOAT, 1, 0, MPI_COMM_WORLD, &requests[0]);\n"
    "    MPI_Wait(&requests[0], &status[0]);\n"
    "}"
))

story.append(h2("4.2  MPI tag assignment"))
story.append(body(
    "Each tensor transferred between devices gets a unique integer MPI tag, assigned "
    "by iterating over all (sender, tensor, receiver) triples in order. "
    "This ensures sends and receives are correctly matched even when multiple tensors "
    "cross the same link."
))

story.append(h2("4.3  main()"))
story.append(body(
    "The generated <code>main()</code> initialises MPI with "
    "<code>MPI_THREAD_MULTIPLE</code> support, reads the image path from argv, "
    "and calls <code>multi_classify()</code>, which dispatches each rank to its "
    "corresponding engine function based on <code>MPI_Comm_rank()</code>."
))
story.append(PageBreak())

# ── Step 5 ──────────────────────────────────────────────────────────────────
story.append(h1("Phase 5 — Compilation"))
story.append(step_table(5, "Compile multinode.cpp into an executable binary",
    "cmake / make builds the multinode binary, linking ncnn, OpenCV, and OpenMPI."))
story.append(space(0.4))

story.append(body(
    "The generated <b>multinode.cpp</b> is compiled as part of the AutoDiCE cmake build. "
    "The CMakeLists.txt in the <code>examples/</code> directory picks it up automatically "
    "because <code>run.sh</code> copies multinode.cpp there before calling make."
))
story.append(code(
    "# run.sh does this:\n"
    "cp models/multinode.cpp ../../../examples/\n"
    "cd ../../../build/ && make -j6\n"
    "cp examples/multinode* ../tools/distributed/vertical/models/"
))
story.append(h2("Key dependencies linked"))
for item in [
    "<b>libncnn</b> — neural network inference (CPU/CUDA layers)",
    "<b>libopenmpi / libmpi_cxx</b> — inter-process communication",
    "<b>libopencv</b> — image loading and preprocessing",
    "<b>libncnn_cuda_lib</b> — optional CUDA acceleration",
]:
    story.append(bullet(item))

story.append(space(0.3))
story.append(note(
    "On heterogeneous setups (x86 laptop + ARM Jetson), multinode.cpp must be "
    "compiled separately on each machine. The same source file is used; cmake detects "
    "the architecture automatically."
))
story.append(PageBreak())

# ── Step 6 ──────────────────────────────────────────────────────────────────
story.append(h1("Phase 6 — Distributed Execution"))
story.append(step_table(6, "Run inference across devices with mpirun",
    "mpirun launches one process per device, each loading its own sub-model and communicating tensors over MPI."))
story.append(space(0.4))

story.append(h2("6.1  Prerequisites"))
for item in [
    "Both machines are reachable by SSH without a password",
    "The <code>models/</code> directory exists at the same absolute path on both machines",
    "Each machine has its own natively compiled <code>multinode</code> binary in that directory",
    "The <code>.param</code> and <code>.bin</code> files for both sub-models are present on both machines (or on a shared NFS mount)",
]:
    story.append(bullet(item))

story.append(h2("6.2  rankfile and hostfile"))
story.append(code(
    "# rankfile — maps MPI rank to hostname and CPU slot\n"
    "rank 0=lenovo    slots=0\n"
    "rank 1=lenovo    slots=1\n\n"
    "# hostfile — list of participating machines\n"
    "lenovo"
))
story.append(body(
    "For a cross-machine setup, replace the hostnames with the actual machine names "
    "or IP addresses and list both in the hostfile:"
))
story.append(code(
    "# rankfile (laptop + jetson)\n"
    "rank 0=laptop-hostname    slots=0\n"
    "rank 1=jetson-hostname    slots=0\n\n"
    "# hostfile\n"
    "laptop-hostname\n"
    "jetson-hostname"
))

story.append(h2("6.3  Launch command"))
story.append(code(
    "cd models/\n"
    "mpirun -rf rankfile ./multinode dog.jpg"
))

story.append(h2("6.4  Execution flow"))
story.append(body("Once launched, the following sequence happens on every inference:"))

flow_data = [
    [Paragraph("<b>Rank 0</b>", ParagraphStyle('r0', fontName='Helvetica-Bold', fontSize=10,
        textColor=colors.HexColor('#1a237e'), alignment=TA_CENTER)),
     Paragraph("", styles['Normal']),
     Paragraph("<b>Rank 1</b>", ParagraphStyle('r1', fontName='Helvetica-Bold', fontSize=10,
        textColor=colors.HexColor('#1a237e'), alignment=TA_CENTER))],
    ["Load sub-model 0\n(.param + .bin)", "←  MPI init  →", "Load sub-model 1\n(.param + .bin)"],
    ["Read & preprocess image", "", "Wait for tensor"],
    ["Run layers 0–17\n→ output fc6_2 tensor", "── fc6_2 (4096 floats) ──►", "Receive fc6_2 tensor"],
    ["", "", "Run layers 18–23\n→ output prob_1"],
    ["", "", "Top-3 classification\nprinted to stderr"],
]
ft = Table(flow_data, colWidths=[5.5*cm, 5*cm, 5.5*cm])
ft.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,0), colors.HexColor('#e8eaf6')),
    ('BACKGROUND', (2,0), (2,0), colors.HexColor('#e8eaf6')),
    ('BACKGROUND', (1,0), (1,0), colors.white),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#fafafa'), colors.white]),
    ('BOX', (0,0), (0,-1), 1, colors.HexColor('#9fa8da')),
    ('BOX', (2,0), (2,-1), 1, colors.HexColor('#9fa8da')),
    ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#e0e0e0')),
    ('FONTSIZE', (0,0), (-1,-1), 9),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ('TEXTCOLOR', (1,2), (1,2), colors.HexColor('#0d47a1')),
    ('FONTNAME', (1,2), (1,2), 'Helvetica-Bold'),
    ('TEXTCOLOR', (1,3), (1,3), colors.HexColor('#0d47a1')),
    ('FONTNAME', (1,3), (1,3), 'Helvetica-Bold'),
]))
story.append(ft)
story.append(space(0.5))

story.append(h2("6.5  Expected output"))
story.append(code(
    "# printed by rank 1 to stderr\n"
    "156 = 0.421500\n"
    "155 = 0.213400\n"
    "285 = 0.098700\n"
    " Blenheim spaniel\n"
    " King Charles spaniel\n"
    " toy spaniel"
))
story.append(PageBreak())

# ── Summary ──────────────────────────────────────────────────────────────────
story.append(h1("Summary"))
story.append(hr())
story.append(space(0.3))

summary_data = [
    [Paragraph("<b>Step</b>", ParagraphStyle('th3', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
     Paragraph("<b>File / Tool</b>", ParagraphStyle('th3', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
     Paragraph("<b>What it does</b>", ParagraphStyle('th3', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white)),
     Paragraph("<b>Outputs</b>", ParagraphStyle('th3', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white))],
    ["1", "interface.py\nmapping.json", "Define partition", "Layer-to-device map"],
    ["2", "onnx_split.py", "Split ONNX graph", "cpu0.onnx, cpu1.onnx\nsender/receiver.json\nrankfile, hostfile"],
    ["3", "onnx2ncnn", "Convert to ncnn", "cpu0.param/.bin\ncpu1.param/.bin"],
    ["4", "interface.py\n(EngineCode)", "Generate C++ runtime", "multinode.cpp"],
    ["5", "cmake / make", "Compile binary", "multinode"],
    ["6", "mpirun", "Run distributed\ninference", "Top-K classification\nresult"],
]
st = Table(summary_data, colWidths=[1.2*cm, 3.8*cm, 4.5*cm, 6.5*cm])
st.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a237e')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f5f5f5'), colors.white]),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#9fa8da')),
    ('INNERGRID', (0,0), (-1,-1), 0.3, colors.HexColor('#c5cae9')),
    ('FONTSIZE', (0,1), (-1,-1), 9),
    ('TOPPADDING', (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('ALIGN', (0,0), (0,-1), 'CENTER'),
]))
story.append(st)
story.append(space(1))
story.append(hr())
story.append(Paragraph(
    "AutoDiCE — Automatic Distributed Inference on Computing Environments",
    ParagraphStyle('footer', fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
))

doc.build(story)
print(f"PDF written to {OUTPUT}")
