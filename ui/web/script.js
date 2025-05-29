
class Commands {
    constructor() {
        this.commands = ["help", "ls", "cd", "pwd", "mkdir", "rm", "cp", "mv", "echo", "clear","touch"];
        this.fs = {
            "/": {
                type: "dir",
                contents: {
                    "home": { type: "dir", contents: {} },
                    "bin": { type: "dir", contents: {} },
                    "file.txt": { type: "file", content: "Contenuto di file.txt" }
                }
            }
        };
        this.currentPath = "/";
    }

    help_command() {
        return this.commands.map(cmd => `- ${cmd}`).join("\n");
    }

    ls_command() {
        const dir = this._resolvePath(this.currentPath);
        if (dir && dir.type === "dir") {
            return Object.keys(dir.contents).join("  ");
        }
        return "Errore: directory non trovata.";
    }

    pwd_command() {
        return this.currentPath;
    }

    cd_command(path) {
        const newPath = this._normalizePath(path);
        const dir = this._resolvePath(newPath);
        if (dir && dir.type === "dir") {
            this.currentPath = newPath;
            return "";
        }
        return `cd: ${path}: No such directory`;
    }

    mkdir_command(name) {
        const dir = this._resolvePath(this.currentPath);
        if (!dir.contents[name]) {
            dir.contents[name] = { type: "dir", contents: {} };
            return "";
        }
        return `mkdir: cannot create directory '${name}': File exists`;
    }

    rm_command(name) {
        const dir = this._resolvePath(this.currentPath);
        if (dir.contents[name]) {
            delete dir.contents[name];
            return "";
        }
        return `rm: cannot remove '${name}': No such file or directory`;
    }

    echo_command(text) {
        return text;
    }

    clear_command() {
        return "__clear__";
    }
    _normalizePath(path) {
        if (path === "..") {
            const parts = this.currentPath.split("/").filter(Boolean);
            parts.pop();
            return "/" + parts.join("/");
        } else if (path.startsWith("/")) {
            return path;
        } else {
            return this.currentPath === "/" ? `/${path}` : `${this.currentPath}/${path}`;
        }
    }

    _resolvePath(path) {
        const parts = path.split("/").filter(Boolean);
        let node = this.fs["/"];
        for (let part of parts) {
            if (!node.contents[part]) return null;
            node = node.contents[part];
        }
        return node;
    }
    touch_command(name) {
        const dir = this._resolvePath(this.currentPath);
        if (!dir.contents[name]) {
            dir.contents[name] = { type: "file", content: "" };
            return "";
        }
        return `touch: cannot create file '${name}': File exists`;
    }
}
document.addEventListener("DOMContentLoaded", () => {
    const input = document.querySelector("#terminal-input");
    const output = document.querySelector("#terminal-output");

    const shell = new Commands();

    input.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            const command = input.value.trim().split(" ");
            const args = command[1];
            let result;

            switch (command[0]) {
                case "help":
                    result = shell.help_command();
                    break;
                case "ls":
                    result = shell.ls_command();
                    break;
                case "cd":
                    result = shell.cd_command(args);
                    break;
                case "pwd":
                    result = shell.pwd_command();
                    break;
                case "mkdir":
                    result = shell.mkdir_command(args);
                    break;
                case "rm":
                    result = shell.rm_command(args);
                    break;
                case "echo":
                    result = shell.echo_command(args);
                    break;
                case "clear":
                    output.innerHTML = ""; 
                    input.value = "";
                    return;
                default:
                    result = `Comando non riconosciuto: ${command[0]}`;
                    break;
            }

            output.innerHTML += `\n$ ${input.value}\n${result}`;
            input.value = "";
            output.scrollTop = output.scrollHeight;
        }
    });
});


window.addEventListener("load", () => {
  window.scrollTo(0, 0);
});

