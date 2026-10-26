"""Educational CPU/computer simulation; does not inspect real hardware."""
from __future__ import annotations

import random
import threading
import time
from dataclasses import dataclass, asdict


@dataclass
class Program:
    id: str
    name: str
    icon: str
    cpu: float
    memory: float
    color: str
    description: str
    running: bool = True


class SimulatedCPU:
    def __init__(self):
        self.lock = threading.RLock()
        self.started = time.monotonic()
        self.last_tick = self.started
        self.programs = {
            "system": Program("system", "Sistema operacional", "🖥️", 3, 780, "#7c8cff", "Serviços essenciais"),
            "browser": Program("browser", "Navegador", "🌐", 12, 1250, "#38bdf8", "Abas e conteúdo web"),
            "chat": Program("chat", "Chat", "💬", 5, 420, "#a78bfa", "Mensagens e chamadas"),
            "blender": Program("blender", "Blender", "🧊", 35, 1800, "#fb923c", "Renderização 3D"),
            "security": Program("security", "Antivírus", "🛡️", 8, 260, "#34d399", "Proteção em segundo plano"),
            "game": Program("game", "Jogo 3D", "🎮", 45, 2200, "#f472b6", "Simulação de jogo"),
            "background": Program("background", "Tarefas em segundo plano", "⚙️", 2, 180, "#94a3b8", "Pequenas tarefas do sistema"),
        }
        self.available = [
            {"id": "editor", "name": "Editor de texto", "icon": "📝", "cpu": 2, "memory": 180, "color": "#facc15", "description": "Edição de texto"},
            {"id": "music", "name": "Reprodutor de música", "icon": "🎵", "cpu": 4, "memory": 240, "color": "#fb7185", "description": "Reprodução de áudio"},
            {"id": "terminal", "name": "Terminal", "icon": "⌨️", "cpu": 1, "memory": 90, "color": "#a3e635", "description": "Linha de comando simulada"},
            {"id": "paint", "name": "Pintura", "icon": "🎨", "cpu": 3, "memory": 300, "color": "#60a5fa", "description": "Desenho e imagens"},
        ]
        self.core_loads = [12.0, 24.0, 9.0, 18.0]
        self.history = []

    def _snapshot_locked(self):
        running = [p for p in self.programs.values() if p.running]
        total_cpu = min(100.0, sum(p.cpu for p in running))
        # Keep a little movement in the demo, without changing the configured program values too much.
        jitter = random.uniform(-2.0, 2.0)
        load = round(max(1.0, min(100.0, total_cpu + jitter)), 1)
        self.core_loads = [round(max(1, min(100, load / 4 + random.uniform(-10, 10))), 1) for _ in range(4)]
        frequency = round(3.2 + (4.0 - 3.2) * min(load / 100, 1), 2)
        temperature = round(35 + load * 0.48 + random.uniform(-1.2, 1.2), 1)
        memory = sum(p.memory for p in running)
        self.history.append({"time": time.strftime("%H:%M:%S"), "cpu": load, "memory": memory})
        self.history = self.history[-30:]
        return {
            "cpu_usage": load,
            "memory_used": memory,
            "memory_total": 8192,
            "frequency": frequency,
            "temperature": temperature,
            "uptime": int(time.monotonic() - self.started),
            "cores": [{"id": i, "load": self.core_loads[i], "frequency": round(frequency * random.uniform(.97, 1.02), 2)} for i in range(4)],
            "threads": 8,
            "programs": [asdict(p) for p in self.programs.values() if p.running],
            "history": list(self.history),
        }

    def snapshot(self):
        with self.lock:
            return self._snapshot_locked()

    def launch(self, program_id):
        with self.lock:
            if program_id in self.programs and self.programs[program_id].running:
                return False, "Esse programa já está aberto."
            template = next((p for p in self.available if p["id"] == program_id), None)
            if template:
                self.programs[program_id] = Program(**template)
                return True, f'{template["name"]} aberto.'
            if program_id in self.programs:
                self.programs[program_id].running = True
                return True, f'{self.programs[program_id].name} aberto.'
            return False, "Programa não encontrado."

    def close(self, program_id):
        with self.lock:
            if program_id == "system":
                return False, "O sistema operacional não pode ser fechado."
            program = self.programs.get(program_id)
            if not program or not program.running:
                return False, "Esse programa não está aberto."
            program.running = False
            return True, f"{program.name} fechado."

    def catalog(self):
        with self.lock:
            running_ids = {p.id for p in self.programs.values() if p.running}
            return [{"id": p["id"], "name": p["name"], "icon": p["icon"], "running": p["id"] in running_ids}
                    for p in self.available] + [
                    {"id": p.id, "name": p.name, "icon": p.icon, "running": p.running}
                    for p in self.programs.values() if p.id not in {x["id"] for x in self.available}
            ]


cpu = SimulatedCPU()
