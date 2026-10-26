Shader "WanxiangGuitu/CatIconStudio" {
 Properties { _BaseColor("Color",Color)=(1,1,1,1) _Metallic("Metallic",Range(0,1))=0 }
 SubShader { Tags { "RenderPipeline"="UniversalPipeline" "RenderType"="Opaque" } Pass {
 HLSLPROGRAM
 #pragma vertex Vert
 #pragma fragment Frag
 #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"
 CBUFFER_START(UnityPerMaterial)
 float4 _BaseColor;float _Metallic;
 CBUFFER_END
 struct A {float4 positionOS:POSITION;float3 normalOS:NORMAL;};
 struct V {float4 positionCS:SV_POSITION;float3 normalWS:TEXCOORD0;};
 V Vert(A v){V o;o.positionCS=TransformObjectToHClip(v.positionOS.xyz);o.normalWS=TransformObjectToWorldNormal(v.normalOS);return o;}
 half4 Frag(V i):SV_Target {float3 n=normalize(i.normalWS);float light=saturate(dot(n,normalize(float3(.35,.65,.7))));float spec=pow(saturate(dot(n,normalize(float3(.3,.45,.85)))),20)*_Metallic*.25;return half4(_BaseColor.rgb*(.5+.5*light)+spec,_BaseColor.a);}
 ENDHLSL
 } }
}
