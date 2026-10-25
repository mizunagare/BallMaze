Shader "Combat/ActorFade" {
 Properties {[MainColor] _BaseColor("颜色",Color)=(1,1,1,1) [MainTexture] _BaseMap("原贴图",2D)="white"{} _CameraFade("遮挡透明度",Range(0,1))=.22}
 SubShader {Tags {"RenderPipeline"="UniversalPipeline" "Queue"="Transparent" "RenderType"="Transparent"}
 Pass {Blend SrcAlpha OneMinusSrcAlpha ZWrite Off Cull Back
 HLSLPROGRAM
 #pragma vertex Vert
 #pragma fragment Frag
 #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
 #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Lighting.hlsl"
 struct A {float4 p:POSITION;float3 n:NORMAL;float2 uv:TEXCOORD0;};struct V {float4 p:SV_POSITION;float3 n:TEXCOORD0;float2 uv:TEXCOORD1;};
 TEXTURE2D(_BaseMap);SAMPLER(sampler_BaseMap);
 CBUFFER_START(UnityPerMaterial)
 half4 _BaseColor;float4 _BaseMap_ST;half _CameraFade;
 CBUFFER_END
 V Vert(A i){V o;o.p=TransformObjectToHClip(i.p.xyz);o.n=TransformObjectToWorldNormal(i.n);o.uv=TRANSFORM_TEX(i.uv,_BaseMap);return o;}
 half4 Frag(V i):SV_Target{half4 c=SAMPLE_TEXTURE2D(_BaseMap,sampler_BaseMap,i.uv)*_BaseColor;Light sun=GetMainLight();c.rgb*=.55h+.45h*saturate(dot(normalize(i.n),sun.direction))*sun.color;c.a*=_CameraFade;return c;}
 ENDHLSL
 }
 }
}
