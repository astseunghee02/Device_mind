# Custom MCP Server

MCP (Model Context Protocol) 서버의 기본 구조입니다.

## 설치

```bash
npm install
```

## 빌드

```bash
npm run build
```

## 개발 모드

```bash
npm run dev
```

## 실행

```bash
npm start
```

## 구조

- `src/index.ts` - 메인 서버 코드
- `package.json` - 프로젝트 설정
- `tsconfig.json` - TypeScript 설정

## 다음 단계

1. `src/index.ts`에서 TODO 주석을 찾아 필요한 도구들을 구현하세요
2. `ListToolsRequestSchema` 핸들러에 도구 정의를 추가하세요
3. `CallToolRequestSchema` 핸들러에 도구 로직을 구현하세요

## Claude Code와 연동

빌드 후, Claude Code 설정에서 다음과 같이 추가할 수 있습니다:

```json
{
  "mcpServers": {
    "custom-server": {
      "command": "node",
      "args": ["/path/to/mcp/dist/index.js"]
    }
  }
}
```
