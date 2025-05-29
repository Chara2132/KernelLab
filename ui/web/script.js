
class Commands {
    constructor() {
        this.commands = ["help", "ls", "cd", "pwd", "mkdir", "rm", "cp", "mv", "echo", "clear"];
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
}

const input = document.getElementById("terminal-input");
const output = document.getElementById("terminal-output");

input.addEventListener("keydown", (event) => {
    const shell = new Commands();

    if (event.key === "Enter") {
        const command = input.value.trim().split(" ");
        const args=command[1];
        switch (command[0]) {
            case "help":
                output = shell.commands.help_command();
                break;
            case "ls":
                output = shell.commands.ls_command();
                break;
            case "cd":
                output = shell.commands.cd_command(args);
                break;
            case "pwd":
                output = shell.commands.pwd_command();
                break;
            case "mkdir":
                output = shell.commands.mkdir_command(args);
                break;
            case "rm":
                output = shell.commands.rm_command(args);
                break;
            case "cp":
                output = shell.commands.cp_command(args);
                break;
            case "mv":
                output = shell.commands.mv_command(args);
                break;
            case "echo":
                output = shell.commands.echo_command(args);
                break;
            case "clear":
                output = shell.commands.clear_command();
                break;
            default:
                output = `Comando non riconosciuto: ${command}`;
                break;
        }

        if (command === "") return;

        output.innerHTML += `\n$ ${command}\n`;
        input.value = "";
        output.scrollTop = output.scrollHeight;
    }
});
