"""Explicit source download. No import-time network or data redistribution."""

import argparse
import hashlib
import json
import shutil
import urllib.request
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", required=True, type=Path, help="New source directory"
    )
    parser.add_argument(
        "--cached", type=Path, help="Use already downloaded files, without network"
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    manifest = []
    for filename, url, sha in SOURCES:
        target = args.output / filename
        if args.cached:
            shutil.copyfile(args.cached / filename, target)
        else:
            with (
                urllib.request.urlopen(url, timeout=120) as source,
                target.open("wb") as out,
            ):
                shutil.copyfileobj(source, out)
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != sha:
            target.unlink()
            raise ValueError("Source checksum mismatch: " + filename)
        manifest.append({"file": filename, "url": url, "sha256": actual})
    (args.output / "source-manifest.json").write_text(json.dumps(manifest, indent=2))
    import torch
    from transformers import MarianConfig, MarianMTModel

    torch.set_num_threads(1)
    # Exact official pinned bytes only. Never load arbitrary pickle weights.
    state = torch.load(
        args.output / "pytorch_model.bin", map_location="cpu", weights_only=True
    )
    model = MarianMTModel(
        MarianConfig.from_pretrained(args.output, local_files_only=True)
    )
    missing, unexpected = model.load_state_dict(state, strict=False)
    if set(missing) - {"lm_head.weight"} or unexpected:
        raise ValueError("Unexpected official state dictionary keys")
    del state
    model.tie_weights()
    model.save_pretrained(args.output, safe_serialization=True)
    (args.output / "pytorch_model.bin").unlink()


SOURCES = [
    (
        "config.json",
        "https://huggingface.co/Helsinki-NLP/opus-mt-en-de/resolve/6183067f769a302e3861815543b9f312c71b0ca4/config.json",
        "f2d6e18ab7a97b96d61484b787aac9cb8d2f7f69731c58cf7f041c89d0512b29",
    ),
    (
        "generation_config.json",
        "https://huggingface.co/Helsinki-NLP/opus-mt-en-de/resolve/6183067f769a302e3861815543b9f312c71b0ca4/generation_config.json",
        "ccb291c223ffca5554af0f6b4d272da15078d2523452c1e39f57247e1dc3e8eb",
    ),
    (
        "pytorch_model.bin",
        "https://huggingface.co/Helsinki-NLP/opus-mt-en-de/resolve/6183067f769a302e3861815543b9f312c71b0ca4/pytorch_model.bin",
        "da068344b1b0c20e6d4a8f77f48e06646b90d679029006b18579e68977206bdd",
    ),
    (
        "source.spm",
        "https://huggingface.co/Helsinki-NLP/opus-mt-en-de/resolve/6183067f769a302e3861815543b9f312c71b0ca4/source.spm",
        "678f2a1177d8389f67b66299762dcc4fc567e89b07e212ba91b0c56daecf47ce",
    ),
    (
        "target.spm",
        "https://huggingface.co/Helsinki-NLP/opus-mt-en-de/resolve/6183067f769a302e3861815543b9f312c71b0ca4/target.spm",
        "bbd1f495eea99c8e21ae086d9146e0fa7b096c3dfdd9ba07ab8b631889df5c9b",
    ),
    (
        "tokenizer_config.json",
        "https://huggingface.co/Helsinki-NLP/opus-mt-en-de/resolve/6183067f769a302e3861815543b9f312c71b0ca4/tokenizer_config.json",
        "052c28be2c51ea3398bf9b9de92004270e29a51f8404f9921ec025986ffbefae",
    ),
    (
        "vocab.json",
        "https://huggingface.co/Helsinki-NLP/opus-mt-en-de/resolve/6183067f769a302e3861815543b9f312c71b0ca4/vocab.json",
        "0d70d89fee4a8b4ef99a56d712163baadcabd5600a597f71515547ee70306329",
    ),
    (
        "README.md",
        "https://huggingface.co/Helsinki-NLP/opus-mt-en-de/resolve/6183067f769a302e3861815543b9f312c71b0ca4/README.md",
        "7625de996b7c4c51c217095941cf2e27d2b5cc5b4cd695c382882679f2f53710",
    ),
    (
        "deu_sentences_detailed.tsv.bz2",
        "https://downloads.tatoeba.org/exports/per_language/deu/deu_sentences_detailed.tsv.bz2",
        "69600c2f96ac4cf5d45fb88f2f469b57aff20b4df15096481ac81c0098e3d38e",
    ),
    (
        "eng_sentences_detailed.tsv.bz2",
        "https://downloads.tatoeba.org/exports/per_language/eng/eng_sentences_detailed.tsv.bz2",
        "3a0e7a2fdd7cbad76f226de4c28371a15a2fc4d115001617288b16a35c6293db",
    ),
    (
        "deu-eng_links.tsv.bz2",
        "https://downloads.tatoeba.org/exports/per_language/deu/deu-eng_links.tsv.bz2",
        "30f79bb84d2b579482bb43b15e90091595bde629063195555aeda535f6ecda2e",
    ),
]

if __name__ == "__main__":
    main()
