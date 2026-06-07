# 부록 6: Quantization

[문서 목차로 돌아가기](../README.md)

## 이 문서를 언제 읽나요?

모델이 메모리에 올라가지 않을 때 quantization이 왜 자주 언급되는지 알고 싶을 때 읽습니다.

## 핵심 요약

Quantization은 model weight를 더 작은 숫자 형식으로 저장해 메모리 사용량을 줄이는 방법입니다.

## 쉬운 설명

정밀도를 낮추면 model이 차지하는 메모리를 줄일 수 있습니다. 하지만 품질과 속도 변화는 model, hardware, quantization 방식에 따라 달라집니다.

```mermaid
flowchart LR
    A[Original weights] --> B[Quantized weights]
    B --> C[Lower memory use]
```

## 실습과 연결되는 지점

이 프로젝트의 기본 경로는 작은 model profile을 사용합니다. quantization은 선택적인 추가 학습 주제로 다룹니다.

## 관련 문서

- [환경 선택](../setup/00_choose_your_environment.md)
- 더 깊이: [심화 8: 양자화 기법](../deep-dive/08_quantization_methods.md)
