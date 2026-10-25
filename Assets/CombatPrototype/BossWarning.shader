Shader "Combat/BossWarning" {
 Properties { [MainColor] _BaseColor("颜色",Color)=(1,1,1,1) }
 SubShader { Tags {"RenderPipeline"="UniversalPipeline" "Queue"="Overlay-20" "RenderType"="Transparent"}
 Pass { Blend SrcAlpha OneMinusSrcAlpha ZWrite Off ZTest Always Cull Off
 HLSLPROGRAM
 #pragma vertex Vert
 #pragma fragment Frag
 #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
 struct A {float4 positionOS:POSITION;half4 color:COLOR;};struct V {float4 positionCS:SV_POSITION;half4 color:COLOR;};
 CBUFFER_START(UnityPerMaterial)
 half4 _BaseColor;
 CBUFFER_END
 V Vert(A i){V o;o.positionCS=TransformObjectToHClip(i.positionOS.xyz);o.color=i.color*_BaseColor;return o;}
 half4 Frag(V i):SV_Target{return i.color;}
 ENDHLSL
 }
 }
}
