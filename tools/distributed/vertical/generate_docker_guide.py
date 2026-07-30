"""Build AutoDiCE_Docker_Guide.pdf — the command reference for running the
vertical-partitioning example inside Docker.

Run it wherever reportlab is available; the container already has it:

    docker run --rm -v $(pwd)/tools/distributed/vertical:/out -w /out \
        autodice python3 generate_docker_guide.py
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER

OUTPUT = "AutoDiCE_Docker_Guide.pdf"

# Courier 8.5pt inside a 17cm frame with 6pt padding fits about 92 characters.
# Code lines are rendered with non-breaking spaces so their alignment survives,
# which means anything longer silently runs off the page — so check as we build.
MAX_CODE_COLS = 88
_overflow = []

INK = colors.HexColor('#1a237e')
INK_SOFT = colors.HexColor('#0d47a1')
RULE = colors.HexColor('#c5cae9')
PANEL = colors.HexColor('#e8eaf6')
BORDER = colors.HexColor('#9fa8da')
MUTED = colors.HexColor('#455a64')

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    'DocTitle', parent=styles['Title'],
    fontSize=26, leading=32, textColor=INK, spaceAfter=6
)
subtitle_style = ParagraphStyle(
    'Subtitle', parent=styles['Normal'],
    fontSize=12, textColor=MUTED, spaceAfter=20, alignment=TA_CENTER
)
h1_style = ParagraphStyle(
    'H1', parent=styles['Heading1'],
    fontSize=16, leading=20, textColor=INK, spaceBefore=14, spaceAfter=6
)
h2_style = ParagraphStyle(
    'H2', parent=styles['Heading2'],
    fontSize=12, leading=16, textColor=INK_SOFT, spaceBefore=10, spaceAfter=4
)
body_style = ParagraphStyle(
    'Body', parent=styles['Normal'],
    fontSize=10, leading=15, spaceAfter=8
)
code_style = ParagraphStyle(
    'Cmd', parent=styles['Code'],
    fontSize=8.5, leading=13, backColor=colors.HexColor('#f5f5f5'),
    borderColor=colors.HexColor('#e0e0e0'), borderWidth=1,
    borderPad=6, spaceAfter=10, fontName='Courier'
)
out_style = ParagraphStyle(
    'Out', parent=code_style,
    backColor=colors.HexColor('#f1f8e9'),
    borderColor=colors.HexColor('#c5e1a5'),
    textColor=colors.HexColor('#33691e')
)
note_style = ParagraphStyle(
    'Note', parent=styles['Normal'],
    fontSize=9, leading=13, textColor=colors.HexColor('#555555'),
    leftIndent=12, spaceAfter=8
)


def esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def h1(text): return Paragraph(text, h1_style)
def h2(text): return Paragraph(text, h2_style)
def body(text): return Paragraph(text, body_style)
def note(text): return Paragraph(f"<i>{text}</i>", note_style)
def space(n=0.3): return Spacer(1, n * cm)
def hr(): return HRFlowable(width="100%", thickness=1, color=RULE, spaceAfter=8)
def mono(text): return f"<font face='Courier'>{esc(text)}</font>"


def code(text, style=code_style):
    """Monospaced block. Spaces become non-breaking so indentation is preserved."""
    lines = text.strip('\n').split('\n')
    for line in lines:
        if len(line) > MAX_CODE_COLS:
            _overflow.append(line)
    rendered = '<br/>'.join(esc(line).replace(' ', '&nbsp;') for line in lines)
    return Paragraph(rendered, style)


def output(text):
    return code(text, out_style)


def grid(headers, rows, widths):
    hdr = [Paragraph(f"<b>{c}</b>", ParagraphStyle(
        'th', fontName='Helvetica-Bold', fontSize=9.5, leading=12,
        textColor=colors.white)) for c in headers]
    data = [hdr]
    for row in rows:
        assert len(row) == len(headers), f"row/header mismatch: {row}"
        data.append([Paragraph(c, ParagraphStyle(
            'td', fontName='Helvetica', fontSize=9, leading=12)) for c in row])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), INK),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, PANEL]),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
    ]))
    return t


def step(number, title, description):
    data = [[
        Paragraph(f"<b>{number}</b>", ParagraphStyle(
            'sn', fontName='Helvetica-Bold', fontSize=14,
            textColor=colors.white, alignment=TA_CENTER)),
        Paragraph(f"<b>{title}</b><br/><font size=9>{description}</font>",
                  ParagraphStyle('sd', fontName='Helvetica', fontSize=10,
                                 leading=14, textColor=INK))
    ]]
    t = Table(data, colWidths=[1.4 * cm, 15.6 * cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), INK),
        ('BACKGROUND', (1, 0), (1, 0), PANEL),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (1, 0), (1, 0), 10),
    ]))
    return t


def callout(title, text, tone='info'):
    bg, edge = {
        'info': (colors.HexColor('#e3f2fd'), colors.HexColor('#90caf9')),
        'warn': (colors.HexColor('#fff8e1'), colors.HexColor('#ffcc80')),
    }[tone]
    p = Paragraph(f"<b>{title}</b><br/><font size=9>{text}</font>",
                  ParagraphStyle('co', fontName='Helvetica', fontSize=10,
                                 leading=14, textColor=colors.HexColor('#263238')))
    t = Table([[p]], colWidths=[17 * cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), bg),
        ('BOX', (0, 0), (-1, -1), 1, edge),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    return t


story = []

# ── Cover ─────────────────────────────────────────────────────────────────────
story += [
    space(2.2),
    Paragraph("AutoDiCE in Docker", title_style),
    Paragraph("Running the distributed AlexNet example — command guide", subtitle_style),
    hr(),
    space(0.4),
    body(
        "AutoDiCE splits a neural network across several compute nodes and runs the pieces "
        "in parallel, passing intermediate results between them over MPI. This guide covers "
        "every command you need to build the image, run the bundled AlexNet example, point it "
        "at your own model, and control which machines the ranks land on."
    ),
    body("Everything runs inside the container. Docker is the only thing you install."),
    space(0.4),
    callout("The short version",
            "Build it once, then run it with your models folder mounted. Models are never "
            "baked into the image, so one image serves any model you give it."),
    space(0.3),
    code("docker build -t autodice .\n"
         "docker run --rm -v $L/models:$V/models:ro -v $L/out:$V/out autodice"),
    space(0.3),
    grid(["What the example does", ""],
         [["Model", f"BVLC AlexNet ({mono('bvlcalexnet-9.onnx')}), 24 layers"],
          ["Split point", f"After {mono('fc6_2')} — 18 layers on rank 0, 6 on rank 1"],
          ["Transferred", f"One tensor, {mono('fc6_2')}, sent rank 0 &#8594; rank 1"],
          ["Input", f"{mono('dog.jpg')}, a retriever photo"],
          ["Output", "Top-3 ImageNet classes"]],
         [4.2 * cm, 12.8 * cm]),
    PageBreak(),
]

# ── 1. Quick start ────────────────────────────────────────────────────────────
story += [
    h1("1. Quick start"),
    body("Run everything from the repository root."),

    h2("Fetch the model"),
    body("The ONNX weights are not in the repository, so this step is not optional on a "
         "fresh clone. About 233 MB."),
    code("mkdir -p $L/models\n"
         "curl -L -o $L/models/bvlcalexnet-9.onnx \\\n"
         "  https://github.com/onnx/models/raw/main/validated/vision/\\\n"
         "classification/alexnet/model/bvlcalexnet-9.onnx"),
    note("The URL is split across lines here to fit the page — join the last two parts "
         "into one address when you paste it."),

    h2("Build the image"),
    body("Once, and again only when you change the source. It compiles the whole ncnn "
         "library, so expect a few minutes."),
    code("cd /home/gkorod/AutoDiCE\ndocker build -t autodice ."),

    h2("Run the example"),
    body("The paths get long, so these two shorthands are used throughout this guide. "
         "Paste them into your shell first, or write the paths out in full."),
    code("L=$(pwd)/tools/distributed/vertical            # on your machine\n"
         "V=/autodice/tools/distributed/vertical        # inside the container"),
    code("docker run --rm -v $L/models:$V/models:ro -v $L/out:$V/out autodice"),
    space(0.1),
    callout("Two folders, one direction each",
            "models/ holds your networks and is only ever read — mount it read-only. "
            "Everything the pipeline generates goes to out/. The models mount is required: "
            "the image contains no networks at all, so without it the run stops with “No "
            "model found”. The out mount is optional — leave it off and the results are "
            "simply discarded with the container."),
    space(0.3),
    body("The last lines you should see:"),
    output("run distributed inference\n"
           "215 = 0.589278\n"
           "207 = 0.127041\n"
           "213 = 0.103414\n"
           " Brittany spaniel\n"
           " golden retriever\n"
           " Irish setter, red setter"),
    body("That is AlexNet classifying the bundled dog photo, with the network split across "
         "two MPI processes."),
    note(f"{mono('--rm')} deletes the container when it exits. Whatever the run generates "
         "survives only in the out/ mount."),

    h1("2. What happens when you run it"),
    body(f"The container's default command is {mono('run.sh')}, which performs four steps "
         "in order:"),
    space(0.1),
    step(1, "Split the model",
         "interface.py reads mapping.json, cuts the ONNX graph into one sub-model per node, "
         "and generates a matching multinode.cpp."),
    space(0.15),
    step(2, "Convert to ncnn",
         "onnx2ncnn turns each sub-model into the .param + .bin pair the inference engine loads."),
    space(0.15),
    step(3, "Compile",
         "multinode.cpp is built into the ./multinode binary, linked against ncnn and MPI."),
    space(0.15),
    step(4, "Run distributed inference",
         "mpirun launches one process per rank. Rank 0 runs the convolutions and sends fc6_2 "
         "to rank 1, which finishes the fully-connected layers and prints the top-3."),
    PageBreak(),
]

# ── 3. Command reference ──────────────────────────────────────────────────────
story += [
    h1("3. Every command, by situation"),
    body(f"All of these assume the {mono('$L')} and {mono('$V')} shorthands from section 1."),

    h2("Run the complete example"),
    body("The normal case. The sub-models, the ncnn weights, the rankfile, the generated "
         "multinode.cpp and the compiled binary all land in out/; models/ is never "
         "written to."),
    code("docker run --rm -v $L/models:$V/models:ro -v $L/out:$V/out autodice"),
    note("Files in out/ are created by root inside the container, so they land on your "
         "disk owned by root."),

    h2("One model in the folder — nothing to configure"),
    body("If the models folder holds exactly one network, that is the one that gets split. "
         "Nothing generated is ever written there, so this stays unambiguous no matter how "
         "many times you run."),
    code("$L/models/               $L/out/\n"
         "  vgg16-7.onnx             lenovo_cpu0.{onnx,param,bin}\n"
         "                           lenovo_cpu1.{onnx,param,bin}\n"
         "                           rankfile, hostfile, sender.json, receiver.json\n"
         "                           multinode.cpp, multinode"),

    h2("Several models in the folder"),
    body("The folder can hold as many networks as you like, but then the choice is "
         f"ambiguous and you have to name one with {mono('AUTODICE_MODEL')}, as a path "
         "relative to the example directory:"),
    code("docker run --rm -v $L/models:$V/models:ro -v $L/out:$V/out \\\n"
         "  -e AUTODICE_MODEL=models/vgg16-7.onnx autodice"),
    body("Without it the run stops and lists what it found, rather than guessing:"),
    output("Several models found in ./models/: bvlcalexnet-9.onnx, vgg16-7.onnx\n"
           "Pick one with AUTODICE_MODEL, e.g.\n"
           "  docker run --rm -e AUTODICE_MODEL=./models/bvlcalexnet-9.onnx ... autodice"),
    note("Remember that mapping.json has to match whichever model you select — the layer "
         "names differ per network. See section 5."),

    h2("Use a models folder from somewhere else entirely"),
    body("Nothing ties the volume to the repository. Point it at any directory."),
    code("docker run --rm -v /data/my-onnx-zoo:$V/models:ro -v $L/out:$V/out \\\n"
         "  -e AUTODICE_MODEL=models/mymodel.onnx autodice"),

    h2("Do you need to clean up between runs?"),
    body("No. There is no container to stop — "
         f"{mono('--rm')} deletes it the moment run.sh finishes — and there is no Docker "
         "volume to remove either, because the mount is a bind mount of a folder on your "
         f"disk, not a named volume. {mono('docker volume ls')} will not show it."),
    body("Nothing accumulates in the models folder, because nothing is ever written there. "
         "Everything in out/ is regenerated and overwritten on each run, so you can leave "
         "it as it is — including when you rename node keys in mapping.json or switch to a "
         "different network."),
    space(0.1),
    body(f"If you want a guaranteed-fresh result anyway, delete the output folder; it is "
         "recreated automatically:"),
    code("rm -rf tools/distributed/vertical/out"),
    note("Sub-models from a previous mapping do stay in out/ under their old names until "
         "you do that. They are never loaded — the run only reads the names currently in "
         "mapping.json — so they waste disk and nothing else."),

    h2("Split the model only, without running inference"),
    body("Useful when you just want to inspect the partition."),
    code("docker run --rm -v $L/models:$V/models:ro -v $L/out:$V/out \\\n"
         "  autodice python3 interface.py"),

    h2("Work inside the container"),
    body("Drops you in a shell at the example directory."),
    code("docker run --rm -it -v $L/models:$V/models:ro -v $L/out:$V/out autodice bash"),
    body("From there:"),
    code("bash run.sh                      # the full pipeline\n"
         "\n"
         "cd out                           # re-run inference only\n"
         "mpirun --allow-run-as-root --oversubscribe \\\n"
         "       -np 2 -rf rankfile ./multinode dog.jpg"),

    h2("Classify a different image"),
    code("docker run --rm -v /path/to/cat.jpg:$V/dog.jpg autodice"),
    PageBreak(),
]

# ── 4. Host names ─────────────────────────────────────────────────────────────
story += [
    h1("4. Choosing which machine each rank runs on"),
    callout("Usually you can skip this section",
            "By default the rankfile is written with the container's own hostname, so a "
            "single-machine run needs no configuration at all. You only need these settings "
            "when the ranks must run on different machines."),
    space(0.35),

    h2("Where the names come from"),
    body(f"Each key in {mono('mapping.json')} has the form "
         f"{mono('<device>_<resource>')}:"),
    code("lenovo_cpu0\n"
         "|_____| |__|\n"
         "   |      +-- cores to pin to     ->  \"slots=0\" in the rankfile\n"
         "   +--------- logical device name ->  which host MPI should use"),
    body("The device part is only a label. Two environment variables decide what real host "
         "it turns into:"),
    grid(["Variable", "What it does"],
         [[mono('AUTODICE_HOST'),
           "One host for every rank. Defaults to the machine's own hostname."],
          [mono('AUTODICE_HOSTS'),
           f"Per-device, comma-separated {mono('device=host')} pairs. Devices not listed "
           f"fall back to {mono('AUTODICE_HOST')}."]],
         [4.6 * cm, 12.4 * cm]),
    space(0.35),

    h2("One device, default — nothing to set"),
    code("docker run --rm autodice"),

    h2("One device, a specific name"),
    body("Both flags are needed and must match: the environment variable decides what goes "
         f"into the rankfile, and {mono('--hostname')} makes the container actually answer "
         "to that name."),
    code("docker run --rm --hostname lenovo -e AUTODICE_HOST=lenovo autodice"),
    note("Set only the environment variable and the rankfile names a host the container is "
         "not. It still runs and still gives the right answer, but prints “not in rankfile, "
         "running without core pinning” and you lose CPU pinning."),

    h2("Several devices, one host each"),
    body(f"With mapping keys {mono('alpha_cpu0')} and {mono('beta_cpu1')}:"),
    code('docker run --rm -e AUTODICE_HOSTS="alpha=node-a,beta=node-b" \\\n'
         '  autodice python3 interface.py'),
    body("produces:"),
    output("--- rankfile ---           --- hostfile ---\n"
           "rank 0=node-a   slots=0    node-a\n"
           "rank 1=node-b   slots=1    node-b"),
    space(0.25),
    callout("Real multi-machine runs need more than names",
            "Setting the hosts tells mpirun where to launch, but getting there also requires "
            "passwordless SSH between the machines (OpenMPI launches remote ranks over SSH, "
            "and this image ships no SSH daemon), the models/ directory present on every host "
            "since each rank loads its own weights from disk, and the MPI port range open "
            "between them.", 'warn'),
    PageBreak(),
]

# ── 5. Your own model ─────────────────────────────────────────────────────────
story += [
    h1("5. Using your own model"),
    body("Nothing in the pipeline is AlexNet-specific. Four steps."),
    space(0.1),
    step(1, "Put your .onnx file in models/", "Alongside the bundled AlexNet."),
    space(0.15),
    step(2, "Get the layer names", "Not the original ONNX node names — see the warning below."),
    space(0.15),
    step(3, "Write mapping.json", "Split the layer list, in order, into one group per node."),
    space(0.15),
    step(4, "Select it with AUTODICE_MODEL",
         "No code change needed — the model is chosen at run time."),
    space(0.35),

    h2("Step 2 in detail"),
    callout("The names are rewritten before splitting",
            "AutoDiCE renames every node to its first output tensor, with slashes turned into "
            "underscores. So the names in mapping.json will not match what you see in Netron. "
            "Always dump them from the formatted model with the command below.", 'warn'),
    space(0.25),
    code('docker run --rm -v $L/models:$V/models:ro autodice python3 -c "\n'
         'from onnx_split import format_onnx\n'
         'import onnx\n'
         "m = onnx.load(format_onnx('models/YOURMODEL.onnx'))\n"
         'print([n.name for n in m.graph.node])"'),
    body("For the bundled AlexNet this prints the same 24 names that appear in mapping.json:"),
    output("['conv1_1', 'conv1_2', 'norm1_1', 'pool1_1', ... ,\n"
           " 'fc6_2', 'fc6_3', 'fc7_1', ... , 'prob_1']"),

    h2("Step 3 in detail"),
    code('{\n'
         '  "lenovo_cpu0": ["conv1_1", "...", "fc6_2"],\n'
         '  "lenovo_cpu1": ["fc6_3", "...", "prob_1"]\n'
         '}'),
    body("Every layer must appear exactly once. The tool checks this and prints "
         f"{mono('Consistency Check Pass.')} — if you miss any, it lists them for you. You are "
         "not limited to two nodes: add more keys and the rankfile, the sends and receives, "
         "and the generated C++ all scale to match."),
    note("Split where the tensor is small. The intermediate blob crosses the network on every "
         "inference, so a fully-connected boundary like fc6_2 costs far less than a cut in the "
         "middle of the convolutional stack."),

    h2("Iterating without rebuilding"),
    body("Mount the files you are editing instead of rebuilding the image each time."),
    code("docker run --rm \\\n"
         "  -v $L/mapping.json:$V/mapping.json \\\n"
         "  -v $L/interface.py:$V/interface.py \\\n"
         "  -v $L/models:$V/models:ro \\\n"
         "  -v $L/out:$V/out \\\n"
         "  autodice"),
    note("Your model also has to survive onnx2ncnn. If it uses operators ncnn does not "
         "implement, conversion prints unsupported-operator warnings and the run fails. That "
         "is an ncnn limitation. AlexNet, VGG and DenseNet are the models this repository has "
         "been exercised on; ResNet needed a fix for its batch dimension."),
    PageBreak(),
]

# ── 6. Troubleshooting ────────────────────────────────────────────────────────
story += [
    h1("6. If something goes wrong"),
    grid(["What you see", "What it means", "What to do"],
         [[mono('not in rankfile, running without core pinning'),
           "The rankfile names a host this machine is not.",
           "Harmless — results are still correct, only CPU pinning is lost. To fix, add "
           f"{mono('--hostname')} matching your {mono('AUTODICE_HOST')}."],
          [mono('mpirun has detected an attempt to run as root'),
           "OpenMPI refuses to run as root by default.",
           f"Add {mono('--allow-run-as-root')}. run.sh already does."],
          [mono('lack of authority to execute on one or more specified nodes'),
           "mpirun cannot reach a host named in the rankfile.",
           "The hostname does not resolve, or SSH is not set up. See section 4."],
          [mono('No model found in ./models/'),
           "The image has no models in it; the volume is missing or empty.",
           f"Add {mono('-v $L/models:$V/models:ro')} and put a .onnx file in it."],
          [mono('Several models found in ./models/'),
           "More than one network in the folder, so the choice is ambiguous.",
           f"Name one with {mono('AUTODICE_MODEL')}, or keep a single model per folder."],
          [mono('failed to bind memory'),
           "Containers cannot bind memory to a NUMA node.",
           "Expected and harmless — CPU pinning still applies. The only way to silence it "
           f"is {mono('--bind-to none')}, which discards the pinning."],
          [mono('Consistency Check Fail.'),
           "mapping.json does not cover the model exactly.",
           "The message lists the missing or extra layers. Every layer, exactly once."],
          [f"Unsupported operator warnings from {mono('onnx2ncnn')}",
           "ncnn has no implementation for an operator in your model.",
           "Use a different model, or replace the operator before exporting."]],
         [4.8 * cm, 4.8 * cm, 7.4 * cm]),

    h1("7. Every environment variable"),
    body("All optional — the defaults are exactly what the quick start uses."),
    grid(["Variable", "Default", "Purpose"],
         [[mono('AUTODICE_MODEL'), "auto-detect",
           "Which network in models/ to split. Only needed when more than one is there."],
          [mono('AUTODICE_IN'), mono('./models'), "Input directory inside the container."],
          [mono('AUTODICE_OUT'), mono('./out'), "Output directory inside the container."],
          [mono('AUTODICE_HOST'), "local hostname", "One MPI host for every rank."],
          [mono('AUTODICE_HOSTS'), "—",
           f"Per-device MPI hosts, e.g. {mono('lenovo=node-a,jetson=node-b')}."]],
         [4.4 * cm, 3.2 * cm, 9.4 * cm]),

    h1("8. Where things live"),
    grid(["Path", "Purpose"],
         [[mono('Dockerfile'),
           "Repository root. Ubuntu 22.04, ncnn + MPI + OpenMP, CPU only."],
          [mono('.dockerignore'),
           "Keeps models/ out of the build context, so the image ships no weights."],
          [mono('tools/distributed/vertical/'),
           "The example. The container starts here."],
          ["&nbsp;&nbsp;" + mono('run.sh'),
           "The four-step pipeline. The image's default command."],
          ["&nbsp;&nbsp;" + mono('interface.py'),
           "Splits the model, generates the C++, writes the rankfile."],
          ["&nbsp;&nbsp;" + mono('mapping.json'),
           "Which layers go to which node. Edit to change the split."],
          ["&nbsp;&nbsp;" + mono('models/'),
           "INPUT. Your ONNX networks. Not in the image — mount it read-only."],
          ["&nbsp;&nbsp;" + mono('out/'),
           "OUTPUT. Everything a run generates. Safe to delete at any time."]],
         [5.6 * cm, 11.4 * cm]),
    space(0.5),
    hr(),
    note("The compiled binary contains no hostnames at all — it dispatches on the MPI rank "
         "number. Only models/rankfile and models/hostfile are host-specific, and you can "
         "edit them by hand after splitting if that is easier than setting the variables."),
]


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(2 * cm, 1.2 * cm, "AutoDiCE — Docker command guide")
    canvas.drawRightString(19 * cm, 1.2 * cm, "%d" % doc.page)
    canvas.setStrokeColor(RULE)
    canvas.line(2 * cm, 1.6 * cm, 19 * cm, 1.6 * cm)
    canvas.restoreState()


doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    rightMargin=2 * cm, leftMargin=2 * cm,
    topMargin=2 * cm, bottomMargin=2 * cm,
    title="AutoDiCE in Docker — command guide",
    author="AutoDiCE",
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)

if _overflow:
    print("WARNING: %d code line(s) exceed %d columns and will overflow:"
          % (len(_overflow), MAX_CODE_COLS))
    for line in _overflow:
        print("  [%d] %s" % (len(line), line))
print("Wrote", OUTPUT)
