"use client";

import { useRef, useState, type KeyboardEvent } from "react";
import type { Procedimento } from "@/lib/procedimentos";
import { IconChevron } from "./Icons";

/** Abas acessíveis (setas do teclado trocam de aba) com perguntas e respostas de cada procedimento. */
export function ProcedimentosTabs({ itens, mostrarConfirmar }: { itens: Procedimento[]; mostrarConfirmar: boolean }) {
  const [ativo, setAtivo] = useState(0);
  const refs = useRef<(HTMLButtonElement | null)[]>([]);

  const onKey = (e: KeyboardEvent) => {
    const passo = e.key === "ArrowRight" || e.key === "ArrowDown" ? 1 : e.key === "ArrowLeft" || e.key === "ArrowUp" ? -1 : 0;
    if (!passo) return;
    e.preventDefault();
    const prox = (ativo + passo + itens.length) % itens.length;
    setAtivo(prox);
    refs.current[prox]?.focus();
  };

  return (
    <div className="grid gap-10 md:grid-cols-[0.9fr_1.4fr] md:gap-16">
      <div role="tablist" aria-label="Procedimentos" aria-orientation="vertical" onKeyDown={onKey} className="-mx-4 flex gap-2 overflow-x-auto px-4 pb-2 [scrollbar-width:none] md:mx-0 md:flex-col md:overflow-visible md:px-0">
        {itens.map((p, i) => (
          <button
            key={p.id}
            ref={(el) => {
              refs.current[i] = el;
            }}
            role="tab"
            id={`tab-${p.id}`}
            aria-selected={i === ativo}
            aria-controls={`painel-${p.id}`}
            tabIndex={i === ativo ? 0 : -1}
            onClick={() => setAtivo(i)}
            className={`min-h-12 shrink-0 rounded-full px-6 text-left text-[0.9375rem] transition-colors md:w-full ${
              i === ativo ? "bg-botao text-white" : "bg-surface text-ink ring-1 ring-line hover:bg-brand-tint"
            }`}
          >
            {p.nome}
          </button>
        ))}
      </div>

      {itens.map((atual, i) => (
        <div
          key={atual.id}
          role="tabpanel"
          id={`painel-${atual.id}`}
          aria-labelledby={`tab-${atual.id}`}
          hidden={i !== ativo}
          tabIndex={0}
          className="rounded-[1.75rem] bg-surface p-6 ring-1 ring-line sm:p-10"
        >
          <h3 className="text-3xl text-ink">
            {atual.nome}
            {mostrarConfirmar && !atual.confirmado && (
              <span className="ml-2 inline-block rounded bg-amber-100 px-1.5 py-0.5 align-middle text-xs font-semibold text-amber-900">CONFIRMAR</span>
            )}
          </h3>
          <p className="mt-4 text-ink-soft">{atual.resumo}</p>
          <div className="mt-8 divide-y divide-line border-y border-line">
            {atual.perguntas.map((q) => (
              <details key={q.pergunta} className="group">
                <summary className="flex min-h-14 cursor-pointer list-none items-center justify-between gap-4 py-4 text-ink">
                  <span>{q.pergunta}</span>
                  <IconChevron className="size-5 text-accent transition-transform group-open:rotate-180" />
                </summary>
                <p className="pb-5 text-ink-soft">{q.resposta}</p>
              </details>
            ))}
          </div>
          <p className="mt-6 text-sm text-ink-soft">Indicado após consulta individual. Os resultados variam de pessoa para pessoa.</p>
        </div>
      ))}
    </div>
  );
}
