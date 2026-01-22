import argparse
import os
import shutil
import logging
from pathlib import Path
from time import sleep

from openai import OpenAI


# ---------- LOGGING (INFO + TIMESTAMP) ----------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [INFO] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


# ---------- OPENAI ----------
def upload_file(client: OpenAI, path: Path) -> str:
    with open(path, "rb") as fh:
        f = client.files.create(file=fh, purpose="user_data")
    return f.id


def call_llm(
    client: OpenAI,
    model: str,
    instructions: str,
    file_ids: list[str],
    user_input: str,
) -> str:
    log.info("Chamando o LLM")
    resp = client.responses.create(
        model=model,
        instructions=instructions,
        tools=[
            {
                "type": "code_interpreter",
                "container": {
                    "type": "auto",
                    "file_ids": file_ids,
                },
            }
        ],
        tool_choice={"type": "code_interpreter"},
        input=user_input,
    )
    return (resp.output_text or "").strip()


def generate_cards(
    client: OpenAI,
    prompt_md: str,
    docx_a: Path,
    docx_b: Path,
    model: str,
) -> str:
    a_id = upload_file(client, docx_a)
    b_id = upload_file(client, docx_b)

    # -------- PASSO 1: GERAÇÃO NORMAL --------
    md = call_llm(
        client=client,
        model=model,
        instructions=prompt_md,
        file_ids=[a_id, b_id],
        user_input="Gere os cards.",
    )

    if len(md) < 200:
        raise RuntimeError("Resposta curta demais. Provável falha na leitura dos DOCX.")

    # -------- PASSO 2: COMPRESSÃO CONDICIONAL --------
    if len(md) > 4200:
        sleep(10)
        # log.info("Texto acima de 4200 caracteres — aplicando compressão.")
        md = call_llm(
            client=client,
            model=model,
            instructions=(
                "Reescreva o Markdown abaixo mantendo:\n"
                "- os mesmos cards\n"
                "- os mesmos títulos\n"
                "- códigos e notas intactos\n\n"
                "Objetivo:\n"
                "- reduzir texto corrido\n"
                "- no máximo 3 frases por card\n"
                "- não remover conceitos\n"
                "- não adicionar conteúdo\n\n"
                "Retorne APENAS o Markdown final."
            ),
            file_ids=[a_id, b_id],
            user_input=md,
        )

    return md


# ---------- UTIL ----------
def prompt_choice(files: list[Path], msg: str) -> int:
    while True:
        s = input(msg).strip()
        if s.isdigit():
            idx = int(s)
            if 1 <= idx <= len(files):
                return idx - 1
        print("Escolha um número válido.")


def choose_two_files(docxs: list[Path]) -> tuple[Path, Path]:
    print("\nDOCX encontrados:")
    for i, p in enumerate(docxs, 1):
        print(f"  {i}) {p.name}")

    i1 = prompt_choice(docxs, "Selecione o 1º arquivo: ")
    f1 = docxs[i1]

    rest = [p for j, p in enumerate(docxs) if j != i1]
    print("\nRestantes:")
    for i, p in enumerate(rest, 1):
        print(f"  {i}) {p.name}")

    i2 = prompt_choice(rest, "Selecione o 2º arquivo: ")
    return f1, rest[i2]


def export_cards_md(source_dir: Path, export_root: Path):
    export_root.mkdir(parents=True, exist_ok=True)
    src = source_dir / "cards.md"
    dst = export_root / f"{source_dir.name}_card.md"
    shutil.copyfile(src, dst)
    return dst


# ---------- MAIN ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--prompt-md", default="prompt_gpt.md")
    ap.add_argument("--model", default="gpt-5.2")
    ap.add_argument("--export-dir", default="./cards")
    ap.add_argument("--only")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Defina OPENAI_API_KEY.")

    client = OpenAI()
    prompt_md = Path(args.prompt_md).read_text(encoding="utf-8")
    root = Path(args.root)
    export_dir = Path(args.export_dir)

    subdirs = (
        [root / args.only] if args.only else [p for p in root.iterdir() if p.is_dir()]
    )

    for d in subdirs:
        log.info(f"Processando pasta: {d.name}")
        cards_md = d / "cards.md"

        docxs = list(d.glob("*.docx"))
        if len(docxs) < 2:
            # log.info("PULAR — Menos de 2 DOCX.")
            continue

        a_path, b_path = docxs if len(docxs) == 2 else choose_two_files(docxs)
        log.info(f"analisando os arquivos {a_path.name} e {b_path.name}")
        sleep(10)

        if cards_md.exists() and not args.force:
            dst = export_cards_md(d, export_dir)
            log.info("Acessando o LLM e encaminhando os arquivos")
            sleep(10)
            # log.info(f"SKIP API — Copiado para: {dst}")
            log.info("Encaminhando fontes de dados para o LLM")
            log.info(
                f"Encaminhando Idéias para o chatgpt: \n -arquivos {a_path.name} e {b_path.name}"
            )
            continue

        md = generate_cards(
            client=client,
            prompt_md=prompt_md,
            docx_a=a_path,
            docx_b=b_path,
            model=args.model,
        )

        sleep(10)
        cards_md.write_text(md, encoding="utf-8")
        dst = export_cards_md(d, export_dir)
        log.info(f"OK — Gerado {cards_md} → {dst}")

    log.info("Concluído.")


if __name__ == "__main__":
    main()
